import asyncio

import io
from django.core.management.base import BaseCommand
from django.core.files import File
from recipes.models import Recipe, Ingredient, RecipeDirection
import aiohttp
from bs4 import BeautifulSoup


class Command(BaseCommand):
    def handle(self, *args, **options):
        main_url = "https://www.povarenok.ru/recipes/~"

        print("parsing recipes")

        loop = asyncio.get_event_loop()
        tasks = [self.get_recipes(main_url, page_num) for page_num in range(1, 10)]
        recipe_dicts = []
        for _recipes in loop.run_until_complete(
                            asyncio.gather(*tasks)):
            recipe_dicts.extend(_recipes)

        print("recipes parsed")
        print("saving recipes to db...")

        counter = 0
        for recipe_dict in recipe_dicts:
            if not recipe_dict['ingredients'] or not recipe_dict['directions']:
                continue

            self.save_recipe_data(recipe_dict)

            counter += 1
            print(f"===== {counter} recipes saved =====", end="\r")
        print()

    async def get_html(self, url: str) -> str:
        connector = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.request('get', url, connector=connector) as response:
            assert response.status == 200
            html = await response.text()
        await connector.close()
        return html

    async def get_recipe_dict(self, recipe_html) -> dict:
        recipe_url = recipe_html.find("a").attrs['href']
        recipe_name = recipe_html.find("h2").text.strip()
        ingredients = [ingr.text for ingr in recipe_html.select(".ings p span a")]
        directions, img_dict = await asyncio.gather(*[self.get_directions(recipe_url),
                                                      self.get_recipe_image(recipe_html)])
        return {"name": recipe_name,
                "ingredients": ingredients,
                "directions": directions,
                "img": img_dict,
                }

    async def get_directions(self, recipe_url: str) -> list:
        html = await self.get_html(recipe_url)
        soup = BeautifulSoup(html, 'lxml')
        return [p.find("p").text for p in soup.select(".cooking-bl")]

    async def get_recipe_image(self, recipe_html) -> dict:
        img_uri = recipe_html.find("img").attrs['src']
        img_filename = img_uri.split("/")[-1]
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.request('get', img_uri, connector=connector) as response:
            assert response.status == 200
            data = await response.read()
        await connector.close()
        io_bytes = io.BytesIO()
        io_bytes.write(data)
        return {"filename": img_filename, "byte_data": io_bytes}

    async def get_recipes(self, main_url, page_num):
        html = await self.get_html(main_url+str(page_num))
        soup = BeautifulSoup(html, "lxml")

        recipes_html = soup.select(".item-bl")
        return await asyncio.gather(*[self.get_recipe_dict(recipe_html)
                                      for recipe_html in recipes_html])

    def save_recipe_data(self, recipe: dict) -> None:
        base_recipe = Recipe(name=recipe['name'])
        base_recipe.save()

        for ingredient in recipe["ingredients"]:
            base_ingr = Ingredient.objects.filter(name=ingredient).first()
            if not base_ingr:
                base_ingr = Ingredient(name=ingredient)
                base_ingr.save()
            base_recipe.ingredients.add(base_ingr)

        for direction_text in recipe["directions"]:
            base_direction = RecipeDirection(text=direction_text, recipe=base_recipe)
            base_direction.save()

        base_recipe.image.save(recipe['img']['filename'], File(recipe['img']['byte_data']))

        base_recipe.save()

