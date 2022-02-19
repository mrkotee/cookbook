from django.contrib import admin
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple
from .models import Recipe, Ingredient, RecipeDirection

# admin.site.register(RecipeDirection)
# class MyModelAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.ManyToManyField: {'widget': CheckboxSelectMultiple},
#     }


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
        ("name", "ingredients"),
    ]
    autocomplete_fields = ["ingredients",]

    inlines = [RecipeDirectionInline]

    search_fields = ("name__contains", "ingredients__name__contains",)

    list_per_page = 30

    list_select_related = True

