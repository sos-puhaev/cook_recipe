from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import RecipeIngredient, Product

@receiver(post_delete, sender=RecipeIngredient)
def update_product_number_cooked_on_delete(sender, instance, **kwargs):
    product = instance.product
    product.number_cooked -= 1
    product.save()
    
@receiver(post_save, sender=RecipeIngredient)
def merge_duplicate_ingredients(sender, instance, **kwargs):
    existing_objects = RecipeIngredient.objects.filter(
        recipe=instance.recipe,
        product=instance.product
    ).exclude(pk=instance.pk)

    for existing_obj in existing_objects:
        if instance.weight_in_grams > existing_obj.weight_in_grams:
            existing_obj.weight_in_grams = instance.weight_in_grams
            existing_obj.save()

            instance.delete()
            break

@receiver(pre_save, sender=Product)
def check_duplicate_product(sender, instance, **kwargs):
    existing_product = Product.objects.filter(name__iexact=instance.name).exclude(pk=instance.pk).first()

    if existing_product:
        raise ValueError(f'Product with name "{instance.name}" already exists.')