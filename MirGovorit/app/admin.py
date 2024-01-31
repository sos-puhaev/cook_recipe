from django.contrib import admin
from .models import Product, Recipe, RecipeIngredient
from .signals import check_duplicate_product

class InlineIngredient(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = [InlineIngredient]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_cooked',)
    readonly_fields = ('number_cooked', )
    
    def save_model(self, request, obj, form, change):
        check_duplicate_product(sender=Product, instance=obj)
        super().save_model(request, obj, form, change)

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'product', 'weight_in_grams',)
