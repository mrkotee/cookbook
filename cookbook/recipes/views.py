from django.shortcuts import render, Http404
from .models import Recipe, Ingredient


def main(request):
    recipes = Recipe.objects.all()
    ingredients = Ingredient.objects.all()

    return render(request, "mainpage.html", {
        "recipes": recipes,
        "ingredients": ingredients,
    })


def recipe_page(request, recipe_id):
    recipe = Recipe.objects.prefetch_related("ingredients").get(pk=recipe_id)

    return render(request, "recipe.html", {
        "recipe": recipe,
    })


def search(request):
    if request.method == "POST":
        recipe_title_part = request.POST.get("recipe_title")
        selected_ingredient = request.POST.get("ingredient")
        query = Recipe.objects.prefetch_related("ingredients")
        if recipe_title_part:
            query = query.filter(name__icontains=recipe_title_part)
        if selected_ingredient:
            ingredient_id = Ingredient.objects.get(name=selected_ingredient).id
            query = query.filter(ingredients__id=ingredient_id)

        recipes = query.all()
        if not recipes:
            return render(request, "not_found.html")
        return render(request, "recipes_grid.html", {
            "recipes": recipes,
        })

    raise Http404
