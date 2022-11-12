from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Recipe,RecipeIngredient

User = get_user_model()

class UsertTest(TestCase):
    def setUp(self):
        self.user_a=User.objects.create_user('cfe',password='abc123')

    def test_user_pwd(self):
        checked = self.user_a.check_password('abc123') 
        self.assertTrue(checked)
        
class RecipeTestCase(TestCase):

    def setUp(self):
        self.user_a=User.objects.create_user('cfe',password='abc123')
        self.recipe_a = Recipe.objects.create(name='Grilled Chicken',user = self.user_a)
        self.recipe_ingredient_a=RecipeIngredient.objects.create(recipe=self.recipe_a, name='Chicken',quantity = '0.5', unit = 'pound')
        self.recipe_ingredient_b=RecipeIngredient.objects.create(recipe=self.recipe_a, name='Chicken',quantity = 'fdgdfg', unit = 'oz')
    
    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(),1)    
    
    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all()
        self.assertEqual(qs.count(),1) 
    
    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs = Recipe.objects.filter(user = user)
        self.assertEqual(qs.count(),1) 
        
    def test_user_recipe_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredient_set.all()
        self.assertEqual(qs.count(),2)   
    def test_user_recipe_ingredient_forward_count(self):
        recipe = self.recipe_a
        qs = RecipeIngredient.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(),2)  
        
    def test_user_two_level_relation(self):
        user = self.user_a   
        qs = RecipeIngredient.objects.filter(recipe__user = user)
        self.assertEqual(qs.count(),2)  
    
    def test_user_one_level_relation_reversed(self):
        user = self.user_a   
        recipe_ingredients_ids = list(user.recipe_set.all().values_list('recipeingredient__id',flat=True))
        qs = RecipeIngredient.objects.filter(id__in=recipe_ingredients_ids)
        self.assertEqual(qs.count(),2)  
    
    def test_unit_measure_validation(self):
        invalid_unit = 'pounds'
        ingredient=  RecipeIngredient.objects.create(recipe=self.recipe_a, name='New',quantity = '0.7', unit = invalid_unit)
        ingredient.full_clean()
        
    def test_unit_measure_validation_error(self):
        invalid_unit = 'xkg'
        with self.assertRaises(ValidationError):
            ingredient=  RecipeIngredient.objects.create(recipe=self.recipe_a, name='New',quantity = '0.7', unit = invalid_unit)
            ingredient.full_clean() 
    
    def test_quantity_as_float(self):
        self.assertIsNotNone(self.recipe_ingredient_a .quantity_as_float)        
        self.assertIsNone(self.recipe_ingredient_b.quantity_as_float)  