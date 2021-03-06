from django.db import models


class TimeStampMixin(models.Model):
    """Add attrs times of creation and update time"""

    created_at = models.DateTimeField("Entry creation time", auto_now_add=True)
    updated_at = models.DateTimeField("Entry last update time", auto_now=True)

    class Meta:
        abstract = True


class Ingredient(models.Model):
    """Ingredients for recipes"""
    name = models.CharField("Name", max_length=60, null=False, unique=True)

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"

    def __str__(self):
        return self.name


class RecipeDirection(models.Model):
    """
    Recipes directions
    _step - numeration of directions
    """
    _step = models.IntegerField(null=True)
    text = models.TextField("Step instruction", null=True)
    recipe = models.ForeignKey("Recipe", related_name="directions", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """if saving new direction automatically numerate _step"""
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

    def __str__(self):
        return f"Step {self._step} of recipe {self.recipe}"


class Recipe(TimeStampMixin):
    """Recipe model.
    Images stores in BASE_DIR/files/media/recipes
    """
    name = models.CharField("Name", max_length=250, null=False)
    ingredients = models.ManyToManyField(Ingredient, verbose_name="Ingredients", related_name="recipes")
    image = models.ImageField("Image", upload_to="recipes", default="logo-white.png")

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ["updated_at"]

    def __str__(self):
        return self.name
