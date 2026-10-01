from django.contrib import admin
from .models import Category, Artwork, ArtworkImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 1

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'price', 'status', 'is_featured')
    list_filter = ('status', 'category')
    inlines = [ArtworkImageInline]
