"""logging_svc_webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r"^$", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r"^$", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r"^blog/", include("blog.urls"))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from logging_svc import views
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from dashboard import urls as dashboard_urls

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"events", views.EventViewSet)
router.register(r"tasks", views.TaskViewSet)
router.register(r"plays", views.PlayViewSet)

schema_view = get_schema_view(title="AnsibleLogServer")
swagger_view = get_swagger_view(title="AnsibleLogServer")

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^api/", include(router.urls)),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^schema/$", schema_view),
    url(r"^api/swagger$", swagger_view),
    url(r'^upload/(?P<filename>[^/]+)$', views.FileUploadView.as_view()),
    url(r"^dashboards/", include(dashboard_urls)),
]
