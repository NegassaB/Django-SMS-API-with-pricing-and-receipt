import requests as request_library


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
            "http://localhost:8055/commons/smsusers/",
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
