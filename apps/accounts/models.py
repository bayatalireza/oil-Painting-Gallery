from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [('buyer','خریدار'),('artist','هنرمند'),('admin','مدیر')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)



    def __ste__(self):
        return self.username

    
class ArtistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist_profile')
    bio = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='artist_covers/', blank=True, null=True)
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    is_approved = models.BooleanField(default=False)  # تایید مدیر برای فروش

    def __str__(self):
        return f"پروفایل هنری {self.user.username}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=150)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    address_line = models.TextField()
    phone_number = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.city} - {self.full_name}"