from django.contrib import admin
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
    readonly_fields = ["created_at",
                       "updated_at"]

    fields = [
        ("name", "ingredients", "image"),
    ]
    autocomplete_fields = ["ingredients",]

    inlines = [RecipeDirectionInline]

    search_fields = ("name__icontains", "ingredients__name__icontains",)

    list_per_page = 30

    list_select_related = True

