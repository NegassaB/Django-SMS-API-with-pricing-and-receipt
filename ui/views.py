from django.shortcuts import render, redirect
import requests as request_library
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse

# Create your views here.

"""
This file is responsible for the entire ui view of the web app.
all user interface/experience is done and used here.
"""


def homepage(request):
    return render(request=request, template_name="ui/homepage.html")


def login_request(request):
    """
    This function is used to login all users except the admin of the entire site.
    It makes an api call to the LoginView defined in commons.apiviews with
    the necessary parameters and renders the necessary html file accordingly.
    It gets the necessary data from the request.session variable.
    """
    if request.method == 'POST':
        # login_response = request_library.Response()
        try:
            user_data = {
                "username": request.POST['username'],
                "password": request.POST['password']
            }

            login_response = request_library.post(
                "http://localhost:8055/commons/login/",
                data=user_data,
                headers={
                    'content-type': "application/x-www-form-urlencoded"
                },
                timeout=(3, 6)
            )
            login_response.raise_for_status()
        except Exception as e:
            # TODO find a better thing to do with the exception
            with open('login_tries.txt', 'a') as login_response_objects:
                login_response_objects.write(str(e) + "\n\n")
        else:
            if login_response is not None:
                # user_token = login_response.token
                messages.info(request, f"You are now logged in as {request.data.get('username')}")
                return redirect('ui/dashboard.html')
            else:
                return HttpResponse("didn't work")

    return render(request=request, template_name="ui/login.html", context={})
