def sender(self, sms_data):
    """
    The actual method that accesses ethio-telecom's server and send the sms.
    It runs on a thread b/c it will recieve multiple requests.
    """
    ethio_telecom_api = "http://10.8.0.86:5000/api/sendsms/"
    header = "content-type": "application/x-www-form-urlencoded"
    request.post(ethio_telecom_api, data={sms_data}, headers=header)


def retry(self, sms_data):
    """
    This method retry's to send the sms in 10 second's time if it has failed via the sender() method.
    """
    ethio_telecom_api = "http://10.8.0.86:5000/api/sendsms/"
    header = "content-type": "application/x-www-form-urlencoded"
    request.post(ethio_telecom_api, data={sms_data}, headers=header)
