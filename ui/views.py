from django.shortcuts import render, redirect
import requests as request_library
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse, HttpResponsePermanentRedirect, FileResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .ui_utilities import check_username_for_registration, check_username, get_total_msgs
from commons.models import SMSMessages, SMSUser, Invoice
from .invoice_generator import generate_invoice

import json

import threading

# Create your views here.

"""
This file is responsible for the entire ui view of the web app.
all user interface/experience is done and used here.
"""


def homepage(request):
    return render(request=request, template_name="ui/index.html")


def login_request(request):
    """
    This function is used to login all users except the admin of the entire site.
    It makes an api call to the LoginView defined in commons.apiviews with
    the necessary parameters and renders the necessary html file accordingly.
    It gets the necessary data from the request.POST variable.
    """
    if request.method == 'POST':
        try:
            # TODO put this into it's own function
            payload = {
                "username": request.POST.get('logusername'),
                "password": request.POST.get('logpassword')
            }

            login_response = request_library.post(
                "http://localhost:8055/commons/login/",
                data=payload,
                headers={
                    'content-type': "application/x-www-form-urlencoded"
                },
                timeout=(3, 6)
            )
            login_response.raise_for_status()
        except Exception as e:
            # TODO find a better thing to do with the exception
            with open('login_tries.txt', 'a') as login_response_objects:
                login_response_objects.write(str(payload['username']) + "\t" + str(e) + "\n\n")

            messages.error(request, "Incorrect username or password")
            return render(request=request, template_name="ui/login.html")
        else:
            if login_response is not None:
                user_token = login_response.text
                #TODO the request.session['is_logged_in'] needs to be upgraded to a better solution
                request.session['is_logged_in'] = True
                messages.success(request, f"You are now logged in as {payload['username']}", fail_silently=True)
                # messages.info(request, f"{user_token}")
                return redirect('ui:dashboard', username=payload['username'])
            else:
                request.session['is_logged_in'] = False
                messages.error(request, "Incorrect username or password")
                return render(request=request, template_name="ui/login.html")
    else:
        # messages.info(request, "Please login")
        return render(request=request, template_name="ui/login.html")
    

def logout_request(request):
    """
    This function is used to logout a user from the web interface.
    """
    if request.session.get('is_logged_in') and request.session['is_logged_in'] == True:
        request.session['is_logged_in'] = False
        del request.session['is_logged_in']
        messages.warning(request, "You have logged out")
        if request.is_ajax():
            return JsonResponse(
                {
                'redirect_url': reverse("ui:login")
                }
            )
        else:
            return redirect("ui:login")
    else:
        messages.error(request, "You need to login first")
        return redirect('ui:login')


def dashboard(request, username):
    """
    This function is used to parse and display the dashboard of the user and his/hers interaction
    with the api.
    If it's redirected from the login, it will get the username and the login status from the request
    and pass that to the dashboard.html template.
    """
    if request.session.get("is_logged_in") and request.session['is_logged_in'] == True:
        user = request.user
        check_username_flag, username_user_token = check_username(username)
        if username and check_username_flag:
          return render(
              request=request,
              template_name="ui/dashboard.html",
              context={
                  "login_successful": True,
                  "username": username,
                  "user_token": username_user_token
              })
        else:
          messages.error(request, "username doesn't exist")
          # return render(request=request, template_name="ui/all404.html", context={"error":"username doesn't exist"})
          return redirect('ui:login')
    else:
        messages.error(request, "You need to login first")
        return redirect('ui:login')


def ajax_dashboard_update(request):
    """
    This function is used to generate the view for the ajax requests that will come from the ui.
    It will get the user token from the ajax request and then gets all the text messages sent by
    that user & the messages sent by that user during the last 5 minutes from the get_total_msgs()
    function declared in ui_utilities. It will also calculate how much has been sent in the last 5 minutes.
    """
    if request.is_ajax() and request.session.get('is_logged_in') and request.session['is_logged_in'] == True:
        # the username of the user that has sent the texts
        ajax_user_token = request.POST.get('ajaxUserToken')
        total_msgs, last5_sent = get_total_msgs(ajax_user_token)
        return JsonResponse(
            {
                'total_msgs': total_msgs,
                'last5_sent': last5_sent
            }
        )
    else:
        return render(request, template_name='ui/dashboard.html', context={})
    


def register_request(request):
    """
    This function is used to register all users from the ui. It first sends the request to
    check_username_for_registration so as to make sure it's a new user. Then it makes
    an api call to the SMSUserCreate defined in commons.apiviews with the necessary
    parameters and renders the necessary html file accordingly. It gets the necessary
    data from the request.POST variable. 
    """
    if request.method == 'POST':
        check_username_result_flag, check_username_result_status_code= check_username_for_registration(request)
        if check_username_result_flag == False:
            try:
                registration_data_payload = {
                    "username": request.POST.get('regusername'),
                    "email": request.POST.get('regemail'),
                    "first_name": request.POST.get('firstname'),
                    "last_name": request.POST.get('lastname'),
                    "company_name": request.POST.get('companyname'),
                    "password": request.POST.get('regpassword')
                }
                
                reg_response = request_library.post(
                    "http://localhost:8055/commons/smsusers/",
                    data=registration_data_payload,
                    headers={
                        'content-type': "application/x-www-form-urlencoded"
                    },
                    timeout=(3, 6)
                )

                reg_response.raise_for_status()
            except Exception as e:
                # seriously do something better with the exception
                with open('registeration_tries.txt', 'a') as reg_tries_object:
                    reg_tries_object.write(str(e) + "\n\n")
                
                messages.error(request, "Unable to register, please try again!")
            else:
                messages.success(request, "Successfully created your sms.et account, please login to your account.")
                return redirect('ui:login')

        elif check_username_result_flag == True:
            messages.error(request, "This username exists, please try again.")
        else:
            # messages.error(request, "Problem encountered, please try again.")
            return render(request=request, template_name="ui/all404.html", context={"error": "Problem encountered, please try again."})

    return render(request=request, template_name="ui/register.html")


def invoice_request(request, username):
    # TODO this might need to change to a webpage that displays all the invoices for a user
    """
    This function is responsible for generating and returning the invoice for each company
    as a pdf.
    """
    if request.session.get('is_logged_in') and request.session['is_logged_in'] == True:
        # thread to run the invoice generation part,
        # decided to run it in crontab instead
        # t = threading.Thread(target=generate_invoice, args=[request, username, "ui/invoice_template.html"])
        # t.setDaemon(True)
        # t.start()
        
        # generate_invoice(request, username, "ui/invoice_template.html")
        user_object = SMSUser.objects.get(username=username)
        all_invoices = Invoice.objects.filter(invoice_to=user_object)
        list_invoices = []
        for single_invoice in all_invoices:
            list_invoices.append(single_invoice.invoice_file)
        
        return render(
            request=request,
            template_name="ui/invoices.html",
            context={
                "list_invoices": list_invoices,
                "username": username
            }
        )
        # ret_val = generate_invoice(request, username, template_name="ui/invoice_template.html")
    else:
        messages.error(request, "You need to login first")
        return redirect('ui:login')


def display_invoice(request, username, slug):
    if request.session.get('is_logged_in') and request.session['is_logged_in'] == True:
        try:
            return FileResponse(open("invoices/" + slug, 'rb'), content_type="application/pdf")
        except Exception as e:
            return render(
                request,
                template_name="ui/all404.html",
                context={
                    "username": username,
                    "error": str(e)
                }
            )


def settings_request(request, username):
    if request.session.get('is_logged_in') and request.session['is_logged_in'] == True:
        return render(
            request,
            template_name="ui/settings.html",
            context={
                "username": username,
            }
        )
    else:
        messages.error(request, "You need to login first")
        return redirect('ui:login')
