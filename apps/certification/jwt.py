from jose import jwt
from .models import CertificationRequest

def verify(token):
    headers = jwt.get_unverified_header(token)
    key = get_key(headers)
    body = jwt.decode(token, key)
    # extend body with headers for validation
    return headers, body

def get_key(headers):
    req = CertificationRequest.objects.get(pk=headers['kid'])
    return req.public_key
