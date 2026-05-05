from svc.utilities.api_key_utils import get_generate_api_key, validate_api_key


def confirm_registration(body, mdns):
    if body and 'api_key' in body:
        validate_api_key(body['api_key'])
        api_key = body['api_key']
    else:
        api_key = get_generate_api_key()
    mdns.unregister()
    return api_key
