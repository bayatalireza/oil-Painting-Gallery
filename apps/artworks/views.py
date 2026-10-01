from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from apps.accounts.decorators import role_required
from .models import Artwork, VisitHistory
from .forms import ArtworkForm, ArtworkImageFormSet

@role_required(['artist', 'admin'])
def artwork_create(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        formset = ArtworkImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            artwork = form.save(commit=False)
            artwork.artist = request.user
            artwork.save()
            formset.instance = artwork
            formset.save()
            messages.success(request, 'اثر با موفقیت ثبت شد.')
            return redirect('artworks:detail', slug=artwork.slug)
    else:
        form = ArtworkForm()
        formset = ArtworkImageFormSet()
    return render(request, 'artworks/artwork_form.html', {'form': form, 'formset': formset})

@role_required(['artist', 'admin'])
def artwork_update(request, slug):
    artwork = get_object_or_404(Artwork, slug=slug)
    if request.user.role != 'admin' and artwork.artist != request.user:
        messages.error(request, 'شما اجازه ویرایش این اثر را ندارید.')
        return redirect('artworks:detail', slug=slug)
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        formset = ArtworkImageFormSet(request.POST, request.FILES, instance=artwork)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'تغییرات ذخیره شد.')
            return redirect('artworks:detail', slug=slug)
    else:
        form = ArtworkForm(instance=artwork)
        formset = ArtworkImageFormSet(instance=artwork)
    return render(request, 'artworks/artwork_form.html', {'form': form, 'formset': formset})

@role_required(['artist', 'admin'])
def artwork_delete(request, slug):
    artwork = get_object_or_404(Artwork, slug=slug)
    if request.user.role != 'admin' and artwork.artist != request.user:
        messages.error(request, 'شما اجازه حذف این اثر را ندارید.')
        return redirect('artworks:detail', slug=slug)
    if request.method == 'POST':
        artwork.delete()
        messages.success(request, 'اثر حذف شد.')
        return redirect('artworks:my_list')
    return render(request, 'artworks/artwork_confirm_delete.html', {'artwork': artwork})

@login_required
def my_artworks(request):
    artworks = Artwork.objects.filter(artist=request.user).order_by('-created_at')
    return render(request, 'artworks/my_artworks.html', {'artworks': artworks})

def artwork_list(request):
    artworks = Artwork.objects.filter(status='available').select_related('artist', 'category')
    return render(request, 'artworks/artwork_list.html', {'artworks': artworks})

def artwork_detail(request, slug):
    artwork = get_object_or_404(Artwork.objects.select_related('artist', 'category'), slug=slug)
    Artwork.objects.filter(pk=artwork.pk).update(views_count=F('views_count') + 1)
    artwork.refresh_from_db()
    VisitHistory.objects.create(
        user=request.user if request.user.is_authenticated else None,
        artwork=artwork,
        ip_address=request.META.get('REMOTE_ADDR'),
    )
    related = Artwork.objects.filter(category=artwork.category, status='available').exclude(pk=artwork.pk)[:4]
    return render(request, 'artworks/artwork_detail.html', {'artwork': artwork, 'related': related})
