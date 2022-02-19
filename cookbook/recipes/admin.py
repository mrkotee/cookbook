from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Recipe, Ingredient, RecipeDirection


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    fields = ['name']
    search_fields = ("name", )
    ordering = ['name']


class RecipeDirectionInline(admin.TabularInline):
    model = RecipeDirection
    extra = 0
    min_num = 2


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    fields = [
        ("name", "ingredients", "image"),
    ]
    autocomplete_fields = ["ingredients",]

    inlines = [RecipeDirectionInline]

    search_fields = ("name__icontains", "ingredients__name__icontains",)

    list_per_page = 30

    list_select_related = True

    list_display = (
        "name",
        "ingrs_list",
    )

    def ingrs_list(self, obj):
        if not obj.ingredients:
            return "-"
        return mark_safe("<br/>".join(str(ingredient) for ingredient in obj.ingredients.all()))

    ingrs_list.short_description = "Ingredients"
