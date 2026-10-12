from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.artworks.models import Artwork
from .models import Cart, CartItem
from django.db import transaction
from apps.artworks.models import Artwork
from .models import Order, OrderItem
from .forms import CheckoutAddressForm, CheckoutPaymentForm



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


@login_required
def checkout_address(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.error(request, 'سبد خرید شما خالی است.')
        return redirect('orders:cart_detail')
    if request.method == 'POST':
        form = CheckoutAddressForm(request.POST)
        if form.is_valid():
            request.session['checkout_address'] = form.cleaned_data['address']
            return redirect('orders:checkout_payment')
    else:
        form = CheckoutAddressForm(initial={'address': request.session.get('checkout_address', '')})
    return render(request, 'orders/checkout_address.html', {'form': form, 'step': 1})

@login_required
def checkout_payment(request):
    if not request.session.get('checkout_address'):
        return redirect('orders:checkout_address')
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        return redirect('orders:cart_detail')
    if request.method == 'POST':
        form = CheckoutPaymentForm(request.POST)
        if form.is_valid():
            # در حالت واقعی اینجا به درگاه (مثل زرین‌پال) وصل می‌شوی؛ فعلاً موفق فرض می‌کنیم
            request.session['checkout_payment'] = form.cleaned_data['payment_method']
            return redirect('orders:checkout_confirm')
    else:
        form = CheckoutPaymentForm()
    return render(request, 'orders/checkout_payment.html', {'form': form, 'step': 2})

@login_required
def checkout_confirm(request):
    address = request.session.get('checkout_address')
    payment = request.session.get('checkout_payment')
    cart = get_object_or_404(Cart, user=request.user)
    items = list(cart.items.select_related('artwork'))
    if not address or not payment or not items:
        messages.error(request, 'اطلاعات تسویه‌حساب ناقص است.')
        return redirect('orders:checkout_address')
    total = sum(item.artwork.price for item in items)
    if request.method == 'POST':
        with transaction.atomic():
            artwork_ids = [item.artwork_id for item in items]
            artworks = Artwork.objects.select_for_update().filter(pk__in=artwork_ids, status='available')
            if artworks.count() != len(items):
                messages.error(request, 'متأسفانه یکی از آثار دیگر موجود نیست.')
                return redirect('orders:cart_detail')
            order = Order.objects.create(user=request.user, total_price=total, address=address, status='paid')
            for art in artworks:
                OrderItem.objects.create(order=order, artwork=art, price=art.price)
            artworks.update(status='sold')
            cart.items.all().delete()
            request.session.pop('checkout_address', None)
            request.session.pop('checkout_payment', None)
        messages.success(request, 'سفارش شما با موفقیت ثبت شد.')
        return redirect('orders:checkout_success', order_id=order.id)
    return render(request, 'orders/checkout_confirm.html',
                  {'items': items, 'total': total, 'address': address, 'payment': payment, 'step': 3})

@login_required
def checkout_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/checkout_success.html', {'order': order})
