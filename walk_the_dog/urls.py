from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_walk", views.new_walk, name="new_walk"),
    path("profile/<int:userID>", views.view_profile, name="view_profile"),
    path("view_dogs", views.view_dogs, name="view_dogs"),
    path("new_dog", views.new_dog, name="new_dog"),

    # API paths
    path("remove_dog/<int:dogID>", views.remove_dog, name="remove_dog"),
    path("delete_walk/<int:walkID>", views.delete_walk, name="delete_walk"),
    path("view_walk/<int:walkID>/", views.view_walk, name="view_walk"),
    path("profile/<int:userID>/get_details", views.get_details, name="get_details"),
    path("profile/<int:userID>/set_image", views.set_image, name="set_image"),
]