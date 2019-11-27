import requests as request_library

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
            return True
        else:
            return False
