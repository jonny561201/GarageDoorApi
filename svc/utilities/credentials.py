import base64


def extract_credentials(bearer_token):
    encoded_token = bearer_token.replace('Basic ', '')
    decoded_token = base64.b64decode(encoded_token).decode('UTF-8')

    credentials = decoded_token.split(':')
    return credentials[0], credentials[1]
