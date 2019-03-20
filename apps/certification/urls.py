from django.urls import include, path
from django.contrib.admin.views.decorators import staff_member_required
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
         staff_member_required(view_func=CertificationView.as_view()),
         name='request-certification'),
]
