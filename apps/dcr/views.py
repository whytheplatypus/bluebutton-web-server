from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, serializers
from oauth2_provider.models import get_application_model
from jose import jwt, jwk
from .models import SoftwareStatement
from apps.certification.jwt import verify

HEADER_CLAIMS = [
    'jwk',
]

REQUIRED_CLAIMS = [
    'redirect_uris',
    # TODO: how to we associate this with a user?
    # interesting problem: user
    'user_id'
]

Application = get_application_model()


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


# class SoftwareStatementSerializer(serializers.Serializer):
#     user = serializers.EmailField()

#     def validate_email(self, value):
#         return User

# TODO update with post + client_id and client_secret basic auth

class Register(APIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def post(self, request, format=None):
        # {
        #    "software_statement" : "{signed software statement}",
        #    "certifications" : [array of one or more signed JWTs],
        #    "udap" : "1"
        # }
        software_jwt  = request.data.get('software_statement')

        certifications = request.data.get('certifications')
        # parse and check software statement
        # TODO: assert that the exp time has not passed and is short
        # (under some configured number of milliseconds)

        # TODO: needs a expiration of it's own that's asserted against
        # TODO: use a x.509 cert
        validator = CertificationValidator(certifications)

        headers, software_statement = validator.verify_software_statement(software_jwt)
        # TODO: verify exp is small enough
        statement_record, created = SoftwareStatement.objects.get_or_create(
            statement=software_statement,
        )
        if created or statement_record.application is None:
            app = Application.objects.create(
                name=software_statement['name'],
                redirect_uris=software_statement['redirect_uris'],
                agree=software_statement['agree'],
                user_id=software_statement['user_id'],
                authorization_grant_type=software_statement['authorization_grant_type'],
                client_type=software_statement['client_type'],
            )
            statement_record.application = app
            statement_record.save()
        else:
            app = statement_record.application
        # respond with credentials
        return Response(ApplicationSerializer(app).data)

class CertificationValidator(object):
    certification_statements = []

    def __init__(self, certifications):
        self.certifications = certifications
        self.verify_certifications()

    def verify_certifications(self):
        for certification in self.certifications:
            _, statement = verify(certification)
            self.certification_statements.append(statement)

    def certify_claim(self, claim, value):
        for cert_statement in self.certification_statements:
            if claim in cert_statement:
                if cert_statement[claim] == value:
                    return True
        return False

    def verify_software_statement(self, jwt_statement):
        headers, body = decode(jwt_statement)
        for claim in REQUIRED_CLAIMS:
            if not self.certify_claim(claim, body[claim]):
                raise Exception("All claims must be certified by all all parties: {}".format(claim))

        for claim in HEADER_CLAIMS:
            if not self.certify_claim(claim, headers[claim]):
                raise Exception("All claims must be certified by all all parties: {}".format(claim))
        return headers, body

def decode(token):
    headers = jwt.get_unverified_header(token)
    key = get_key(headers)
    body = jwt.decode(token, key)
    # extend body with headers for validation
    return headers, body

def get_key(headers):
    # jwks_uri = headers['jwks_uri']
    # keys = headers['jwks']
    # kid = headers['kid']
    return headers['jwk']
