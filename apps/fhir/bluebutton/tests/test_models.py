from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from apps.test import BaseApiTest

from ..models import Crosswalk
from ...server.models import ResourceRouter


class TestModels(BaseApiTest):
    def test_get_full_url_good(self):
        # Create a user
        user = self._create_user('john', 'password',
                                 first_name='John',
                                 last_name='Smith',
                                 email='john@smith.net')
        # created a default user
        fs = ResourceRouter.objects.create(name="Main Server",
                                           fhir_url="http://localhost:8000/fhir/",
                                           shard_by="Patient",
                                           server_search_expiry=1800)

        cw = Crosswalk.objects.create(user=user,
                                      fhir_source=fs,
                                      fhir_id="-20000000000001",
                                      user_id_hash="139e178537ed3bc486e6a7195a47a82a2cd6f46e911660fe9775f6e0dd3f1130")

        fhir = Crosswalk.objects.get(user=user.pk)

        url_info = fhir.get_fhir_patient_url()

        expected_result = '{}{}/{}'.format(fs.fhir_url, fs.shard_by, cw.fhir_id)
        self.assertEqual(url_info, expected_result)

    def test_get_full_url_bad(self):
        # Create a user
        user = self._create_user('john', 'password',
                                 first_name='John',
                                 last_name='Smith',
                                 email='john@smith.net')

        # created a default user
        fs = ResourceRouter.objects.create(name="Main Server",
                                           fhir_url="http://localhost:8000/fhir/",
                                           shard_by="Patient",
                                           server_search_expiry=1800)

        Crosswalk.objects.create(user=user,
                                 fhir_source=fs,
                                 fhir_id="-20000000000001",
                                 user_id_hash="139e178537ed3bc486e6a7195a47a82a2cd6f46e911660fe9775f6e0dd3f1130")

        fhir = Crosswalk.objects.get(user=user.pk)

        url_info = fhir.get_fhir_patient_url()

        invalid_match = "http://localhost:8000/fhir/" + "Practitioner/123456"
        self.assertNotEqual(url_info, invalid_match)

    def test_require_user_id_hash(self):
        user = self._create_user('john', 'password',
                                 first_name='John',
                                 last_name='Smith',
                                 email='john@smith.net')
        with self.assertRaises(IntegrityError):
            Crosswalk.objects.create(user=user)

    def test_immutable_fhir_id(self):
        user = self._create_user('john', 'password',
                                 first_name='John',
                                 last_name='Smith',
                                 email='john@smith.net')

        # created a default user
        fs = ResourceRouter.objects.create(name="Main Server",
                                           fhir_url="http://localhost:8000/fhir/",
                                           shard_by="Patient",
                                           server_search_expiry=1800)

        Crosswalk.objects.create(user=user,
                                 fhir_source=fs,
                                 fhir_id="-20000000000001",
                                 user_id_hash="139e178537ed3bc486e6a7195a47a82a2cd6f46e911660fe9775f6e0dd3f1130")
        cw = Crosswalk.objects.get(_fhir_id="-20000000000001")
        with self.assertRaises(ValidationError):
            cw.fhir_id = "-20000000000002"


    def test_immuatble_user_id_hash(self):
        user = self._create_user('john', 'password',
                                 first_name='John',
                                 last_name='Smith',
                                 email='john@smith.net')

        # created a default user
        fs = ResourceRouter.objects.create(name="Main Server",
                                           fhir_url="http://localhost:8000/fhir/",
                                           shard_by="Patient",
                                           server_search_expiry=1800)

        cw = Crosswalk.objects.create(user=user,
                                 fhir_source=fs,
                                 fhir_id="-20000000000001",
                                 user_id_hash="139e178537ed3bc486e6a7195a47a82a2cd6f46e911660fe9775f6e0dd3f1130")
        cw = Crosswalk.objects.get(_fhir_id="-20000000000001")
        self.assertEqual(cw.user_id_hash, "139e178537ed3bc486e6a7195a47a82a2cd6f46e911660fe9775f6e0dd3f1130")
        with self.assertRaises(ValidationError):
            cw.user_id_hash = "239e178537ed3bc486e6a7195a47a82a2cd6f46e911660fe9775f6e0dd3f1130"
