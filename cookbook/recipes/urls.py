from django.urls import path, include
from .views import main, recipe

urlpatterns = [
    path('', main),
    path('recipe', recipe),
]
