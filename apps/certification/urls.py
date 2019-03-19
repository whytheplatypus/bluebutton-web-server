from django.urls import include, path
from rest_framework import routers
from .views import (
    RequestView,
    CertificationView,
)


router = routers.SimpleRouter()
router.register(r'requests', RequestView)

urlpatterns = router.urls
urlpatterns += [
    path('certify/<int:pk>/',
         CertificationView.as_view(),
         name='request-certification'),
]
