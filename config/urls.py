"""URL routing: everything the mobile app uses lives under /api/."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("candidates.urls")),
]
