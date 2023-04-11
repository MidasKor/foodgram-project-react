from django.contrib import admin
from django.utils.html import format_html

from .models import Recipe, Ingredient, IngredientAmount, Tag, Favorite


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_image', 'cooking_time')
    list_filter = ('author', 'tags')
    search_fields = ('title', 'author__username', 'tags__name')
    autocomplete_fields = ('author', 'tags')

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        else:
            return ''
    get_image.short_description = 'Изображение'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__title')

