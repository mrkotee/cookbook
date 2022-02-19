
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include, reverse
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", RedirectView.as_view(url="recipes")),
    path("recipes/", include("recipes.urls"), name="recipes"),
]

"""add static and media to urlpatterns, while starting without WSGI and NGINX"""
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
