
from oauth2_provider.validators import URIValidator
from oauth2_provider.validators import urlsplit

from oauth2_provider.settings import oauth2_settings
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
import re


class RedirectURIValidator(URIValidator):
    def __init__(self, allowed_schemes):
        self.allowed_schemes = allowed_schemes

    def __call__(self, value):
        super(RedirectURIValidator, self).__call__(value)
        value = force_text(value)
        if len(value.split('#')) > 1:
            raise ValidationError('Redirect URIs must not contain fragments')
        scheme, netloc, path, query, fragment = urlsplit(value)

        # Fix the mobile endpoint validation
        # Allow 2 character alpha plus 8 numerics
        if scheme.lower() in self.allowed_schemes:
            pass

        elif scheme.lower() not in self.allowed_schemes:
            raise ValidationError('Invalid Redirect URI:[%s]' % scheme.lower())


def validate_uris(value):
    """
    This validator ensures that `value` contains valid blank-separated URIs"
    """
    v = RedirectURIValidator(oauth2_settings.ALLOWED_REDIRECT_URI_SCHEMES)
    for uri in value.split():
        regex = set_regex()
        if compare_to_regex(regex, uri):
            pass
        else:
            v(uri)


def set_regex():
    return r'\b[a-zA-Z]{2}[0-9]{8}\b'


def compare_to_regex(regex, uri):
    """

    :param regex:
    :param uri:
    :return:
    """
    if re.findall(regex, uri):
        return True
    else:
        return False
