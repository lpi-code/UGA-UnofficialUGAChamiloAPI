import requests

def check_chamilo_login_state(response):
    """
    Return true if the response given doesn't correspond to a logged out web page
    """

    return "alert alert-danger" in response.text
