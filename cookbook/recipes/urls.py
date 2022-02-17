from django.urls import path, include
from .views import main, get_recipe

urlpatterns = [
    path('', main),
    path('recipe/<int:recipe_id>', get_recipe),
]
