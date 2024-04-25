from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='/login/')
def movies(request):
    if request.method =="POST":
        data=request.POST
        
        movie_name=data.get('movie_name')
        movie_details=data.get('movie_details')
        movie_image=request.FILES.get('movie_image')

        Movie.objects.create(
            movie_name=movie_name,
            movie_details=movie_details,
            movie_image=movie_image,
            )

        return redirect('/movies/') 
    
    queryset= Movie.objects.all()

    if request.GET.get('search'):
        queryset=queryset.filter(movie_name__icontains=request.GET.get('search'))
        

    context={'movies': queryset}

    return render(request, 'movies.html',context)
@login_required(login_url='/login/')
def update_movie(request, id):
    queryset= Movie.objects.get(id=id)

    if request.method=="POST":
        data=request.POST
        movie_name=data.get('movie_name')
        movie_details=data.get('movie_details')
        movie_image=request.FILES.get('movie_image')


        queryset.movie_name=movie_name
        queryset.movie_details=movie_details

        if movie_image:
            queryset.movie_image=movie_image

        queryset.save()
        return redirect('/movies/')

    context={'movies': queryset}

    return render(request, 'update.html', context)

@login_required(login_url='/login/')
def delete_movie(request, id):
    queryset= Movie.objects.get(id=id)
    queryset.delete()
    return redirect('/movies/')


def login_page(request):
    if request.method =="POST":
        
        username = request.POST.get('username')
        password = request.POST.get('password')


        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")

            return redirect('/login/')
        
        user = authenticate(username=username,password=password)

        if user is None:
            messages.error(request,'Invalid Password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/movies/')


    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register(request):

    if request.method =="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')


        if not (first_name and last_name and username and password):
            messages.error(request, "All fields must be filled.")
            return redirect('/register/')


        user=User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "Username already taken.")
            return redirect('/register/')

        user= User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,

        )

        user.set_password(password)
        user.save()

        messages.info(request, "Account created successfully.")
        

        return redirect('/register/')


    return render(request, 'register.html')
    