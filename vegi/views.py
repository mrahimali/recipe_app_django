from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login/')
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


def login_page(req):
    if req.method=='POST':
        username=req.POST.get('user_name')
        password=req.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(req,'Invalid Username')
            return redirect('/login/')
        user =authenticate(username=username, password=password)

        if user is None:
            messages.error(req, 'Invalid Password')
            return redirect('/login/')
        else:
            login(req, user)
            return redirect('/recipes/')

    return render(req, 'login.html')

def signup_page(req):
    if req.method=='POST':
        first_name=req.POST.get('first_name')
        last_name=req.POST.get('last_name')
        user_name=req.POST.get('user_name')
        password=req.POST.get('password')
        c_password=req.POST.get('c_password')

        user=User.objects.filter(username=user_name)
        if user.exists():
            messages.add_message(req, messages.INFO, "Username Exist !!!")
            return redirect('/signup/')

        if(password == c_password):
            user=User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=user_name,
            )
            user.set_password(password)
            user.save()
            messages.add_message(req, messages.INFO, "Account created successfully!!!.")
            return redirect('/login/')

    return render(req, 'register.html')


def logout_page(request):
    logout(request)
    return redirect('/login/')