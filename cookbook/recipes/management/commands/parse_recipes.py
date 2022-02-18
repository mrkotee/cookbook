from django.core.management.base import BaseCommand
from recipes.models import Recipe, Ingredient, RecipeDirection
# from django.core.files import File
# import os
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    def handle(self, *args, **options):
        main_url = "https://www.povarenok.ru/recipes/~"

        ingredients = Ingredient.objects

        counter = 0
        for page_num in range(1, 10):
            res = requests.get(main_url+str(page_num))
            soup = BeautifulSoup(res.content, 'lxml')

            recipes = soup.select(".item-bl")
            for recipe in recipes:
                recipe_url = recipe.find("a").attrs['href']
                recipe_name = recipe.find("h2").text.strip()

                base_recipe = Recipe(name=recipe_name)
                base_recipe.save()

                for ingr in recipe.select(".ings p span a"):
                    base_ingr = ingredients.filter(name=ingr.text).first()
                    if not base_ingr:
                        base_ingr = Ingredient(name=ingr.text)
                        base_ingr.save()
                    base_recipe.ingredients.add(base_ingr)

                for direction_text in self.get_directions(recipe_url):
                    base_direction = RecipeDirection(text=direction_text, recipe=base_recipe)
                    base_direction.save()

                base_recipe.save()
                counter += 1
                print(f"===== {counter} recipes load =====", end="\r")
        print()

    def get_directions(self, recipe_url):
        res = requests.get(recipe_url)
        soup = BeautifulSoup(res.content, 'lxml')
        for p in soup.select(".cooking-bl"):
            yield p.find("p").text



