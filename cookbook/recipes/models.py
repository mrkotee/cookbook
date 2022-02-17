from django.db import models


class TimeStampMixin(models.Model):
    """Реализация атрибутов времени создания и обновления записи"""

    created_at = models.DateTimeField("Время создания записи", auto_now_add=True)
    updated_at = models.DateTimeField("Время обновления записи", auto_now=True)

    class Meta:
        abstract = True


class Ingredient(models.Model):
    """Ingredients for recipes"""
    name = models.CharField("Название", max_length=120, null=False)
    units = models.CharField("Единицы измерения", max_length=15, null=False)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


# class RecipeIngredient(Ingredient):
#     """Recipe ingredients"""
#     ingredient = models.ForeignKey("Ingredient", null=False, on_delete=models.PROTECT)
#     amount = models.DecimalField("Количество", max_digits=6, decimal_places=2, null=False)
#     recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)


class Recipe(TimeStampMixin):
    """Recipes"""
    name = models.CharField("Название", max_length=250, null=False)
    description = models.TextField("Описание")
    instruction = models.TextField("Инструкция по приготовлению")

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name
