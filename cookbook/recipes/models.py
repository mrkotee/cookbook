from django.db import models


class TimeStampMixin(models.Model):
    """Реализация атрибутов времени создания и обновления записи"""

    created_at = models.DateTimeField("Время создания записи", auto_now_add=True)
    updated_at = models.DateTimeField("Время обновления записи", auto_now=True)

    class Meta:
        abstract = True


class Ingredient(models.Model):
    """Ingredients for recipes"""
    name = models.CharField("Название", max_length=60, null=False, unique=True)

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

class RecipeDirection(models.Model):
    _step = models.IntegerField(null=True)
    text = models.TextField()
    recipe = models.ForeignKey("Recipe", related_name="directions", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet
            recipe_steps = RecipeDirection.objects.filter(recipe=self.recipe).all()
            if not recipe_steps:
                self._step = 1
            else:
                self._step = len(recipe_steps) + 1

        super(RecipeDirection, self).save(*args, **kwargs)

    @property
    def step(self):
        return self._step

    # @step.setter
    # def step(self, value):
    #     recipe_steps = RecipeDirection.objects.filter(recipe=self.recipe).all()
    #
    #     if value > len(recipe_steps):
    #         return None
    #     existing_step = recipe_steps.filter(_step=self._step).first()
    #     if existing_step:
    #         return None
    #     self._step = value
    #     self.save()


class Recipe(TimeStampMixin):
    """Recipes"""
    name = models.CharField("Название", max_length=250, null=False)
    ingredients = models.ManyToManyField(Ingredient, verbose_name="Ингредиенты", related_name="recipes")

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["updated_at"]

    def __str__(self):
        return self.name
