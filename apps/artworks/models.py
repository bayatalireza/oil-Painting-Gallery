from django.db import models
from django.core.exceptions import ValidationError
from apps.accounts.models import User
from .validators import validate_artwork_image

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self): return self.name

class Artwork(models.Model):
    STATUS_CHOICES = [
        ('available', 'موجود'),
        ('sold', 'فروخته شده'),
        ('reserved', 'رزرو شده'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artworks')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='artworks')
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=0)
    width = models.PositiveIntegerField(verbose_name='عرض (سانتی‌متر)')
    height = models.PositiveIntegerField(verbose_name='ارتفاع (سانتی‌متر)')
    technique = models.CharField(max_length=100, verbose_name='تکنیک')
    year_created = models.PositiveIntegerField(verbose_name='سال خلق')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    main_image = models.ImageField(upload_to='artworks/main/', validators=[validate_artwork_image])
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.title

class ArtworkImage(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='artworks/gallery/', validators=[validate_artwork_image])
    caption = models.CharField(max_length=200, blank=True)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'artwork')

class VisitHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    visited_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
