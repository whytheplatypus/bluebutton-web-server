import requests
from django import forms
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
        FormView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import (
    viewsets,
    serializers,
    permissions,
    mixins,
)
from .models import CertificationRequest


class CertificationRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = CertificationRequest
        fields = (
            'id',
            'software_statement',
            'created', 'signed',
            'token',
            'public_key',
            'certified_by',
        )
    
    def create(self, validated_data):
        instance, _ = CertificationRequest.objects.get_or_create(**validated_data)
        return instance
            

class RequestView(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    queryset = CertificationRequest.objects.all()
    serializer_class = CertificationRequestSerializer


# class CeritificationsView(TemplateView):
#     template_name = "certifications.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['certifications'] = CertificationRequest.objects.all()
#         return context


class CertificationForm(forms.Form):
    name = forms.BooleanField(label="I approve this name")
    tos = forms.BooleanField(label="I approve these terms of service")
    redirect_uris = forms.BooleanField(label="I approve these redirect uris")


class CertificationView(LoginRequiredMixin, FormView):
    template_name = "certification.html"
    form_class = CertificationForm
    success_url = '/v1/certification/requests/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['certification_request'] = CertificationRequest.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        request = CertificationRequest.objects.get(pk=self.kwargs.get('pk'))
        request.sign(self.request.user)
        cred_callback = request.software_statement.get("certification_callback", False)
        if cred_callback:
            requests.post(cred_callback, data={"certification": request.token})
        return super().form_valid(form)
