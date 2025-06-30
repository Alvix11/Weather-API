def handle_errors(response):
    if response.status_code == 404:
        return "Page not found"
    elif response.status_code == 500:
        return "A general error occurred while processing the request."
    elif response.status_code == 400:
        return "The format of the API is incorrect or an invalid parameter or combination of parameters was supplied."
    elif response.status_code == 401:
        return"There is a problem with the API key, account or subscription."
    elif response.status_code == 429:
        return "The account has exceeded their assigned limits."
    elif response.status_code != 200:
        return f"Unexpected error: {response.status_code}"
    return None