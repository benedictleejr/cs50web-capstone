import json
from os import error, name
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Date_of_walks, User, Dog, Walk
from datetime import datetime, timedelta

# Create your views here.
def index(request):
  userID = request.user.id

  todays_date = datetime.now().strftime("%A %d %B %Y")

  dates = Date_of_walks.objects.all().order_by('date')
  paginator = Paginator(dates, 7)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(request, "walk_the_dog/index.html", {
    'page_obj': page_obj,
    'todays_date': todays_date,
    'userID': userID,
  })

def login_view(request):
  if request.method == "POST":

    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "walk_the_dog/login.html", {
            "message": "Invalid username and/or password."
        })
  else:
    return render(request, "walk_the_dog/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
  if request.method == "POST":
    username = request.POST["username"]
    email = request.POST["email"]

    # Ensure password matches confirmation
    password = request.POST["password"]
    confirmation = request.POST["confirmation"]
    if password != confirmation:
      return render(request, "walk_the_dog/register.html", {
          "message": "Passwords must match."
      })

    # Attempt to create new user
    try:
      user = User.objects.create_user(username, email, password)
      user.save()
    except IntegrityError:
      return render(request, "walk_the_dog/register.html", {
          "message": "Username already taken."
      })
    login(request, user)
    return HttpResponseRedirect(reverse("index"))
  else:
    return render(request, "walk_the_dog/register.html")
  

# API function
def view_walk(request, walkID):
  try:
    walk = Walk.objects.get(pk=walkID)
    walkers = walk.walked_by.all()
    if walkers.exists():  # Check if there are any walkers associated
      walked_by = walkers[0].username
    else:
      walked_by = None  # Handle case where no walkers are associated
    
    data = {
      'date': walk.date,
      'time': walk.time,
      'duration': walk.duration,
      'dog_walked': walk.dog_walked.name,
      'walked_by': walked_by,
      'completed': walk.completed,
    }
    return JsonResponse(data)
  except Walk.DoesNotExist:
    return JsonResponse({'error': 'Walk not found'}, status=404)
  

def view_profile(request, userID):
  user = User.objects.get(id=userID)
  username = user.username
  walks_completed = user.num_walks.count()
  picture = user.picture

  return render(request, "walk_the_dog/profile.html", {
    "user": user,
    "username": username,
    "walks_completed": walks_completed,
    "picture": picture,
  })

# API function
def get_details(request, userID):
  try:
    user = User.objects.get(id=userID)
    data = {
      "username": user.username,
      "email": user.email,
      "walks": user.num_walks.count(),
      "picture_url": user.picture if user.picture else ''
    }
    return JsonResponse(data)
  except User.DoesNotExist:
    return JsonResponse({'error': 'User not found'}, status=404)

# API function
@login_required
def set_image(request, userID):
  if request.method == 'POST':
    user = User.objects.get(id=userID)
    if request.user != user:
      return JsonResponse({'success': False, 'error': 'You are not allowed to edit this profile.'})

    data = json.loads(request.body)
    new_url = data.get('new_url', '')
    user.picture = new_url
    user.save()
    return JsonResponse({'success': True, 'new_url':new_url})
  else:
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@login_required
def new_walk(request):
  dogs = Dog.objects.all()
  users = User.objects.all()

  if request.method == "POST":
    date = request.POST.get("date")
    time = request.POST.get("time")
    duration_mins = request.POST.get("duration")
    walker_id = request.POST.get("walked_by")
    dog_id = request.POST.get("dog")
    completed_OnOff = request.POST.get("completed") # Checkbox returns "on" if checked
    completed = True if completed_OnOff == "on" else False 

    if date and time and duration_mins and dog_id:
      try:
        duration_seconds = int(duration_mins) * 60  # Convert duration(mins) to seconds
        duration = timedelta(seconds=duration_seconds) # converts seconds into a time the database can store

        if duration_seconds <= 0:
          raise ValueError("Duration must be greater than 0.")
        
        # Save the new walk
        new_walk = Walk.objects.create(
          date=date,
          time=time,
          duration=duration,
          dog_walked=Dog.objects.get(id=dog_id),
          completed=completed,
        )
        walked_by = User.objects.get(pk=walker_id)
        new_walk.walked_by.add(walked_by)
        new_walk.save()

        # if Date_of_walks object exists with the same date, just return
        date_objs = Date_of_walks.objects.filter(date=new_walk.date)
        if date_objs.exists():
          date_obj = date_objs.first()
          date_obj.walks.add(new_walk)
          date_obj.number_of_walks += 1
          date_obj.save()
          return HttpResponseRedirect(reverse("index"))
        
        else: # else we must create new one
          new_date_obj = Date_of_walks.objects.create(
            date=new_walk.date
          )
          new_date_obj.walks.add(new_walk)
          new_date_obj.number_of_walks += 1
          new_date_obj.save()
          return HttpResponseRedirect(reverse("index"))
    
      except ValueError:
        return render(request, "walk_the_dog/new_walk.html", {
          "users": users,
          "dogs": dogs,
          "message": "Invalid duration value.",
        })
      except Dog.DoesNotExist:
        return render(request, "walk_the_dog/new_walk.html", {
          "users": users,
          "dogs": dogs,
          "message": "Selected dog does not exist.",
        })

    else:
      return render(request, "walk_the_dog/new_walk.html", {
        "users": users,
        "dogs": dogs,
        "message": "Please fill in all required fields.",
      })
  else:
    return render(request, "walk_the_dog/new_walk.html", {
      "users": users,
      "dogs": dogs,
    })

def delete_walk(request, walkID):
  try:
    walk = Walk.objects.get(pk=walkID)  # Retrieve the Walk object by its primary key
    walk.delete()  # Delete the Walk object
    return JsonResponse({'success': True})
  except error as e:
    return JsonResponse({'success': False, 'error': e})

def view_dogs(request):
  dogs = Dog.objects.all()
  paginator = Paginator(dogs, 7)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(request, "walk_the_dog/view_dogs.html", {
    "page_obj": page_obj,
  })

def new_dog(request):
  if request.method == "POST":
    name = request.POST['name']
    breed = request.POST['breed']
    age = int(request.POST['age'])
    picture = request.POST['picture']
    special_instructions = request.POST['special_instructions']
    dog = Dog(name=name, breed=breed, age=age, picture=picture, special_instructions=special_instructions)
    dog.save()
    owners = request.POST.getlist('owners')
    for owner_id in owners:
      user = User.objects.get(id=owner_id)
      dog.owners.add(user)
    dog.save()
    return HttpResponseRedirect(reverse('view_dogs'))
  else:
    users = User.objects.all()
    return render(request, 'walk_the_dog/new_dog.html', {'users': users})
  
def remove_dog(request, dogID):
  try:
    dog = Dog.objects.get(pk=dogID)
    dog.delete()  # Delete the Walk object
    return JsonResponse({'success': True})
  except error as e:
    return JsonResponse({'success': False, 'error': e})