from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    def __str__(self):
        return self.user.username

    # This field is required.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar', default="avatar/profileIcon.jpeg")
    friends = models.ManyToManyField(User, blank=True, related_name="UserFriend")

    gender_choices = (("1", "male"), ("2", "female"),)

    # Other fields here
    gender = models.CharField(max_length=5, choices=gender_choices, default="male")
    location = models.CharField(max_length=100, default="Empty")
    favorite_animal = models.CharField(max_length=20, default="Dragons")
    job = models.CharField(max_length=50, default="Empty")
    education = models.CharField(max_length=50, default="Empty")
    short_description = models.TextField(default="Empty")

    def create_user_profile(sender, created, instance, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User, weak=False)
