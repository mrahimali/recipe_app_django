from django.shortcuts import render, redirect
from .models import *

# Create your views here.


def recipes(req):
    
    if req.method=='POST':
        data=req.POST
        recipe_name=data.get('recipe_name')
        recipe_description=data.get('recipe_description')
        recipe_image=req.FILES['recipe_image']
        print(recipe_name)
        print(recipe_description)
        print(recipe_image)

        Recipe.objects.create(
            recipe_name= recipe_name,
            recipe_description= recipe_description,
            recipe_image= recipe_image
        )

        return redirect('/recipes/')

    queryset= Recipe.objects.all()

    if req.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains=req.GET.get('search'))
    context={'recipes': queryset}
    return render(req, 'recipes.html', context)


def delete_recipe(req, id):
    recipe=Recipe.objects.get(id=id)
    recipe.delete()
    return redirect('/recipes/')

def update_recipe(req, id):
    recipe=Recipe.objects.get(id=id)

    if req.method =='POST':
        data=req.POST
        recipe_name=data.get('recipe_name')
        recipe_description=data.get('recipe_description')
        recipe_image=req.FILES.get('recipe_image')

        recipe.recipe_name=recipe_name
        recipe.recipe_description= recipe_description
        if recipe_image:
            recipe.recipe_image=req.FILES['recipe_image']

        recipe.save()
        return redirect('/recipes/')


    context={'recipe': recipe}
    return render(req, 'update_recipe.html', context)