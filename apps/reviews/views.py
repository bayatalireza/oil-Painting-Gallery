from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.artworks.models import Artwork
from .forms import ReviewForm
from .models import Review

@login_required
def add_review(request, slug):
    artwork = get_object_or_404(Artwork, slug=slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.update_or_create(
                artwork=artwork, user=request.user,
                defaults={'rating': form.cleaned_data['rating'],
                          'comment': form.cleaned_data['comment'],
                          'is_approved': False},
            )
            messages.success(request, 'نقد شما ثبت شد و پس از تأیید نمایش داده می‌شود.')
    return redirect('artworks:detail', slug=slug)
