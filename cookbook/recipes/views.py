from django.shortcuts import render
from .models import Recipe, Ingredient


def main(request):
    recipes = Recipe.objects.all()
    return render(request, "mainpage.html", {
        "recipes": recipes,
    })


def get_recipe(request, recipe_id):
    recipe = Recipe.objects.prefetch_related("ingredients").get(pk=recipe_id)

    # ingredients = recipe.ingredients

    return render(request, "recipe.html", {
        "recipe": recipe,
    })
