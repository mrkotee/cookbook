from django.urls import path, include
from .views import main, recipe_page, search

urlpatterns = [
    path('', main),
    path('recipe/<int:recipe_id>', recipe_page),
    path('search/', search),
]
