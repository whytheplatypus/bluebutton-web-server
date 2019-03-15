from jose import jwt, jwk
from .models import CertificationRequest

def verify(token):
    headers = jwt.get_unverified_header(token)
    key = get_key(headers)
    body = jwt.decode(token, key)
    # extend body with headers for validation
    return headers, body

def get_key(headers):
    req = CertificationRequest.objects.get(pk=headers['kid'])
    public_key = req.public_key
    RSAKey = jwk.get_key('RS256')
    pk_jwk = RSAKey(public_key, 'RS256').to_dict()
    return pk_jwk
