from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.artworks.models import Artwork
from .models import Cart, CartItem

@login_required
def cart_add(request, artwork_id):
    if request.method != 'POST':
        return redirect('artworks:list')
    artwork = get_object_or_404(Artwork, pk=artwork_id, status='available')
    if artwork.artist == request.user:
        messages.error(request, 'نمی‌توانید اثر خودتان را بخرید.')
        return redirect('artworks:detail', slug=artwork.slug)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, artwork=artwork)
    if created:
        messages.success(request, 'اثر به سبد خرید اضافه شد.')
    else:
        messages.info(request, 'این اثر قبلاً در سبد خرید شماست.')
    return redirect('orders:cart_detail')

@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('artwork')
    total = sum(item.artwork.price for item in items)
    return render(request, 'orders/cart_detail.html', {'items': items, 'total': total})

@login_required
def cart_remove(request, item_id):
    if request.method != 'POST':
        return redirect('orders:cart_detail')
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    item.delete()
    messages.success(request, 'اثر از سبد حذف شد.')
    return redirect('orders:cart_detail')

