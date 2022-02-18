from django.shortcuts import render, Http404
from .models import Recipe, Ingredient, RecipeDirection


def main(request):
    recipes = Recipe.objects.all()
    ingredients = Ingredient.objects.all()

    return render(request, "mainpage.html", {
        "recipes": recipes,
        "ingredients": ingredients,
    })


def recipe_page(request, recipe_id):
    recipe = Recipe.objects.prefetch_related("ingredients").prefetch_related("directions").get(pk=recipe_id)

    return render(request, "recipe.html", {
        "recipe": recipe,
    })


def search(request):
    if request.method == "POST":
        recipe_title_part = request.POST.get("recipe_title")
        selected_ingredients = request.POST.getlist("ingredients[]")

        query = Recipe.objects.prefetch_related("ingredients")
        if recipe_title_part:
            query = query.filter(name__icontains=recipe_title_part)
        if selected_ingredients:
            for ingredient_name in selected_ingredients:
                ingredients_id = Ingredient.objects.get(name=ingredient_name).id
                query = query.filter(ingredients=ingredients_id)

        recipes = query.all()
        if not recipes:
            return render(request, "not_found.html")
        return render(request, "recipes_grid.html", {
            "recipes": recipes,
        })

    raise Http404
