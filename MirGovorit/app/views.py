from typing import Any
from django.views.generic import TemplateView
from .models import Recipe, Product, RecipeIngredient
from django.db.models import Subquery, Q

class ViewCookBook(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs: Any):  
        context = super().get_context_data(**kwargs)
        
        context['recipes'] = Recipe.objects.all()
        context['products'] = Product.objects.all()
        
        form_type = self.request.GET.get('form_type')
        if form_type == 'form1':
            recipe_id = self.request.GET.get('recipes')
            product_id = self.request.GET.get('products')
            weight_in_grams = self.request.GET.get('weight_in_grams')
        
            context['result_send'] = self.add_product_to_recipe(recipe_id, product_id, weight_in_grams)
            
        elif form_type == 'form2':
            recipe_id = self.request.GET.get('recipes')
            try:
                recipe_id = int(recipe_id)
                self.cook_recipe(recipe_id)
            except (TypeError, ValueError):
                print("Error form2")
        
        elif form_type == 'form3':
            product_id = self.request.GET.get('products')
            try:
                product_id = int(product_id)
                context['table_show'] = self.show_recipes_without_product(product_id)
                print(context['table_show'])
            except (TypeError, ValueError):
                print("Error form 3")
                
        return context
    
    def add_product_to_recipe(self, recipe_id, product_id, weight):
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            product = Product.objects.get(id=product_id)
            
            recipe_ingredient = RecipeIngredient.objects.filter(recipe=recipe, product=product).first()

            if recipe_ingredient:
                if recipe_ingredient.weight_in_grams < int(weight):
                    recipe_ingredient.weight_in_grams = weight
                    recipe_ingredient.save()
                    return f"Successfully updated {product.name} in {recipe.name} with {weight} grams."
                else:
                    return f"No update needed for {product.name} in {recipe.name}. Weight in DB is greater or equal."
            else:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    product=product,
                    weight_in_grams=weight
                )
                self.cook_recipe(recipe_id)
                return f"Successfully added {product.name} to {recipe.name} with {weight} grams and increased number_cooked."

        except Recipe.DoesNotExist:
            return "Recipe does not exist."
        except Product.DoesNotExist:
            return "Product does not exist."
    
    def cook_recipe(self, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            products_in_recipe = recipe.ingredients.all()

            for product in products_in_recipe:
                product.number_cooked += 1
                product.save()

            return f"Successfully cooked recipe {recipe.name}. Number_cooked for all products increased."

        except Recipe.DoesNotExist:
            return "Recipe does not exist."
        
    def show_recipes_without_product(self, product_id):
        recipes_with_low_weight = RecipeIngredient.objects.filter(
            product=product_id,
            weight_in_grams__lt=10
        ).values('recipe_id')

        recipes_info = Recipe.objects.filter(id__in=recipes_with_low_weight).values('id', 'name')
        recipes_info = list(recipes_info)

        recipes_without_product = Recipe.objects.exclude(
            Q(id__in=Subquery(recipes_with_low_weight)) |
            Q(recipeingredient__product=product_id)
        ).values('id', 'name')

        combined_recipes = recipes_info.copy()
        combined_recipes.extend(recipes_without_product)

        return combined_recipes
