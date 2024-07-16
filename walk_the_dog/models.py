from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

# Create your models here.
class User(AbstractUser):
  # Already have username, email, and password
  num_walks = models.ManyToManyField('Walk', blank=True, related_name="walked_by")
  picture = models.URLField(max_length=200, blank=True, null=True)

  def __str__(self):
    return self.username
    
class Dog(models.Model):
  name = models.CharField(max_length=64)
  breed = models.CharField(max_length=64)
  age = models.IntegerField()
  owners = models.ManyToManyField(User, blank=True, related_name="dogs")
  picture = models.URLField(max_length=500, blank=True, null=True)
  special_instructions = models.TextField(blank=True, null=True)

  def __str__(self):
    return f"{self.name}"

class Walk(models.Model):
  walkID = models.AutoField(primary_key=True)
  date = models.DateField(default=now)
  time = models.TimeField(default=now, )
  duration = models.DurationField(help_text="HH:MM:SS")
  dog_walked = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name="walks", verbose_name="Dog Walked")
  completed = models.BooleanField(default=False)

  def __str__(self):
    return f"Walk on {self.date} at {self.time} with {self.dog_walked}"
  
class Date_of_walks(models.Model):
  date = models.DateField(default=now)
  walks = models.ManyToManyField(Walk, blank=True, related_name="dates")
  number_of_walks = models.IntegerField(default=0)

  def __str__(self):
    return f"{self.date}"