from django.contrib import admin
from .models import Date_of_walks, User, Dog, Walk

class DogAdmin(admin.ModelAdmin):
  filter_horizontal = ("owners",)
  list_display = ["name", "breed", "age", "owners"]

# Register your models here.
admin.site.register(User)
admin.site.register(Dog)
admin.site.register(Walk)
admin.site.register(Date_of_walks)