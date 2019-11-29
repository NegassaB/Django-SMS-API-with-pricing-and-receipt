import requests as request_library
from rest_framework.authtoken.models import Token
from commons.models import SMSUser

import json

base_url = "http://localhost:8055/"

"""
This file is responsible for providing a checking mechanism to the ui.views file.
Especially in regards to login, logout, register etc.
"""

def check_username_for_registration(request):
    """
    This function is responsible for checking the registration details of a new smsuser
    against the commons database. It will send a get request to the api endpoint and
    parse it's response accordingly.
    Whatever the results, it will return the status_code of check_username_response.
    """
    while request.POST is not None:
        username = request.POST.get('regusername')
        break
    
    try:
        check_username_response = request_library.get(
            base_url + "commons/smsusers/",
            headers={
                'content-type': "application/x-www-form-urlencoded"
            },
            timeout=(3, 6)
        )
        check_username_response.raise_for_status()
    except Exception as e:
        with open('check_username_tries.txt', 'a') as cut_object:
            cut_object.write(str(e) + "\n\n")
            return False, e.response.status_code
    else:
        if username in check_username_response.text:
            # returns True if the username is in the system, thus telling the view to skip this one
            return True, check_username_response.status_code
        else:
            return False, check_username_response.status_code


def check_username(username):
    # TODO: check if this can't be done by the above function
    """
    This function is used to check if the provided username actually exists in the
    database for the dashboard function found in the ui/views.py. While that
    may seem unnecessary considering that the dashboard is called from the login_request
    function, since the url parameter can be edited and thus allow an attacker to gain
    access to our or the user's system we will have to re-check if the provided username
    actually does exist within our system.
    It will send a get request to the api endpoint and parse it's response accordingly. It
    then checks if the username provided is in the response object and if it is returns a True
    value. If it's not it returns a False value.
    It will also return the user_token for that username so as it can be used in the dashboard.
    """
    username_to_check = username
    try:
        check_username_for_existence = request_library.get(
            base_url + "commons/smsusers/",
            headers={
                'content-type': "application/x-www-form-urlencoded"
            },
            timeout=(3, 6))
    except Exception as e:
        with open('check_username_existence_tries.txt', 'a') as cuet_object:
            cuet_object.write(str(e) + "\n\n")
            return False
    else:
        if username_to_check in check_username_for_existence.text:
            return True, get_user_token(username_to_check)
        else:
            return False


def get_user_token(username):
    """
    This function is responsible for getting the user token from the database
    by searching using the username. The way it's works is, it searches for
    that user in the SMSUser model first and uses that object to search for
    the token key from the Token model. There might be a better way of doing
    this than the way I did it below but since time is running out I have to do
    it this way and then try to improve it in the future.
    """
    return Token.objects.get(user=SMSUser.objects.get(username=username))


def get_total_msgs(user_token):
    """
    This function is called by  the ajax_dashboard_update function from the views module.
    It sums up all the sms text messages sent by the user identified by the user_token.
    """
    try:
        get_msgs = request_library.get(
            base_url + "notification/sendsms/",
            headers=
            {
                'content-type': "application/x-www-form-urlencoded",
                'authorization': "token " + user_token
            },
            timeout=(3, 6)
        )
    except Exception as e:
        with open('get_user_sent_messages_tries.txt', 'a') as gusm_object:
            gusm_object.write(str(e) + "\n\n")
    else:
        # it counts the number of unique ids' are in the response meaning
        # there amount of text message sent.
        counter = 0
        json_data = json.loads(get_msgs.text)
        for result in json_data['result_objects']:
            if result['id']:
                counter += 1
        
        return counter
