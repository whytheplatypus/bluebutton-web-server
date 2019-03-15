from jose import jwt
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from Crypto.PublicKey import RSA


class CertificationRequest(models.Model):
    software_statement = JSONField()
    # TODO Encrypt this
    private_key = models.BinaryField(null=True) # keep hidden?
    token = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    signed = models.DateTimeField(null=True)

    def sign(self):
        key = RSA.generate(2048)
        self.private_key = key.export_key()

        headers = {
            'kid': self.id,
        }
        
        self.token = jwt.encode(
            self.software_statement,
            self.private_key,
            algorithm='RS256',
            headers=headers)

        self.signed = timezone.now()
        self.save()
        return self.token

    @property
    def public_key(self):
        key = RSA.importKey(bytes(self.private_key))
        return key.publickey().export_key()
