import pathlib
import pint
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from .utils import number_str_to_float
from .validators import validate_unit_of_measure

"""
manager
"""
class RecipeQuerySet(models.QuerySet):
    '''
    possible to do objects.filter('t').search('...')
    '''
    def search(self,q=None):
        if q is None or q == '':
            return self.none()
        lookup =  (
                    Q(name__icontains=q) | 
                    Q(description__icontains=q)|
                    Q(directions__icontains=q)
                )
        return self.filter(lookup)

class RecipeManager(models.Manager):
    
    def get_queryset(self):
        return RecipeQuerySet(self.model,using=self._db)
    
    def search(self,q=None):
        return self.get_queryset().search(q=q)
"""
end manager
"""

class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True)
    
    objects = RecipeManager()

    @property
    def title(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"id": self.id})

    def get_hx_url(self):
        return reverse("recipes:hx-detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("recipes:update", kwargs={"id": self.id})
    
    def get_delete_url(self):
        
        return reverse("recipes:delete", kwargs={"id": self.id})

    def get_ingredients_children(self):
        return self.recipeingredient_set.all()
    
    
def recipe_ingredient_image_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1()) # uuid1->uuid + timestamp
    return f"recipes/ingredient/{new_fname}{fpath.suffix}"
    
    
class RecipeIngredientImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    image= models.ImageField(upload_to=recipe_ingredient_image_upload_handler)
    

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50)  # 1 1/4
    quantity_as_float = models.FloatField(blank=True, null=True)
    # pounds, lbs, oz, gram, etc
    unit = models.CharField(max_length=50, validators=[validate_unit_of_measure])
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return self.recipe.get_absolute_url()
    
    def get_delete_url(self):
        kwargs = {
            "parent_id": self.recipe.id,
            "id": self.id
        }
        return reverse("recipes:ingredient-delete", kwargs=kwargs)

    def get_hx_edit_url(self):
        kwargs = {
            "parent_id": self.recipe.id,
            "id": self.id
        }
        return reverse("recipes:hx-ingredient-detail", kwargs=kwargs)

    def convert_to_system(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit]
        return measurement #.to_base_units()

    def as_mks(self):
        # meter, kilogram, second
        measurement = self.convert_to_system(system='mks')
        return measurement.to_base_units()

    def as_imperial(self):
        # miles, pounds, seconds
        measurement = self.convert_to_system(system='imperial')
        return measurement.to_base_units()


    def save(self, *args, **kwargs):
        qty = self.quantity
        qty_as_float, qty_as_float_success = number_str_to_float(qty)
        if qty_as_float_success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)

# class RecipeImage():
#     recipe = models.ForeignKey(Recipe)