from django.http import HttpRequest

def get_basic_auth_from_header(request: HttpRequest):
    """Gets the basic auth from the Authorization: Basic header

    Args:
    - request (HttpRequest)

    Returns:
    - (tuple(string, string)): the basic auth information in the form (client_id, client_secret)
    """
    try:
        print(request.headers)
        header  = request.headers.get('Authorization').split()
        basic   = header[0]
        creds   = header[1]
        if basic.lower() != 'basic':
            raise Exception('Authorization header was not in the correct format')

        creds = creds.split(':')
        return (creds[0], creds[1])
    except:
        return None
