from jose import jwt, jwk
from django.utils import timezone
from datetime import timedelta
from oauth2_provider.compat import parse_qs, urlparse
from oauth2_provider.models import (
    get_application_model,
    get_access_token_model,
)
from django.urls import reverse

from apps.test import BaseApiTest

from Crypto.PublicKey import RSA

from apps.certification.models import CertificationRequest


Application = get_application_model()


class TestDynamicClientRegistration(BaseApiTest):
    def test_app_creation(self):
        user = self._create_user('anna', '123456')

        key = RSA.generate(2048)
        private_key = key.export_key()

        public_key = key.publickey().export_key()
        RSAKey = jwk.get_key('RS256')
        pk_jwk = RSAKey(public_key, 'RS256').to_dict()
        pk_jwk['n'] = pk_jwk['n'].decode("utf-8") 
        pk_jwk['e'] = pk_jwk['e'].decode("utf-8")

        headers = {
            'jwk': pk_jwk,
        }

        software_statement = {
            'name': 'DCRTestApp',
            'redirect_uris': 'http://localhost:8000',
            'agree': True,
            'user_id': user.id,
            'jwk': pk_jwk,
        }
        software_jwt = jwt.encode(software_statement, private_key, algorithm='RS256', headers=headers)

        # TODO configure trust framework in settings: TrustFramework.verify(jwt)
        req = CertificationRequest.objects.create(software_statement=software_statement)

        certification_jwts = [
            req.sign(),
        ]

        response = self.client.post('/v1/o/register', {
            'software_statement': software_jwt,
            'certifications': certification_jwts,
        })

        self.assertEqual(response.status_code, 200)
        app = response.json()
        self.assertTrue('client_id' in app)
        self.assertTrue('client_secret' in app)

        # Test that posting again simply returns the same app
        response = self.client.post('/v1/o/register', {
            'software_statement': software_jwt,
            'certifications': certification_jwts,
        })

        self.assertEqual(response.status_code, 200)
        app_again = response.json()
        self.assertDictEqual(app, app_again)


    def test_dev_exp_too_short(self):
        return
        software_statement = {
            'name': 'DCRTestApp',
            'redirect_uri': 'http://localhost:8000',
            'agree': True,
            'exp': 'some bad time',
        }
        software_jwt = jwt.encode(software_statement, 'secret', algorithm='HS256')
        certification_jwts = [
            jwt.encode(software_statement, 'secret', algorithm='HS256')
        ]
        response = self.client.post('/v1/o/register', {
            'software_statement': software_jwt,
            'certifications': certification_jwts,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.status_code, 400)

    def test_cert_exp_passed(self):
        pass
