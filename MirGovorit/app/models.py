from django.db import models

class Product(models.Model):
    name = models.CharField(max_length = 255)
    number_cooked = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    name = models.CharField(max_length = 255)
    ingredients = models.ManyToManyField('Product', through='RecipeIngredient')

    def __str__(self):
        return self.name
    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight_in_grams = models.IntegerField()

    def __str__(self):
        return f"{self.recipe.name} {self.product.name} ({self.weight_in_grams})"
