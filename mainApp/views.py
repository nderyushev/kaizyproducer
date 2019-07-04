from django.shortcuts import render
from django.http import  HttpResponseRedirect, JsonResponse, Http404
from .models import *

def get_or_create_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.beats.count()
        request.session['total_price'] = float(sum([cart_item.beat.price for cart_item in cart.beats.all()]))
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    return cart

def base_view(request):
    cart = get_or_create_cart(request)
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'base.html', context)

def category_view(request, category_slug):
    cart = get_or_create_cart(request)
    category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all()
    beats_in_category = Beat.objects.all().filter(category_id=category.id)
    context = {
        'category': category,
        'categories': categories,
        'beats_in_category': beats_in_category
    }
    return render(request, 'category.html', context)

def cart(request):
    cart = get_or_create_cart(request)
    beats = Beat.objects.all()
    total_price = 0.00
    for beat in cart.beats.all():
        total_price += float(beat.item_total)
    context = {
        'cart': cart,
        'beats': beats,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)


def add_to_cart(request):
    cart = get_or_create_cart(request)
    beat_slug = request.GET.get('beat_slug')
    beat = Beat.objects.get(slug=beat_slug)
    cart.add_to_cart(beat.slug)
    new_cart_total = 0.00
    for beat in cart.beats.all():
        new_cart_total += float(beat.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.beats.count(), 'cart_total_price': cart.cart_total})

def remove_from_cart(request):
    cart = get_or_create_cart(request)
    beat_slug = request.GET.get('beat_slug')
    beat = Beat.objects.get(slug=beat_slug)
    cart.remove_from_cart(beat.slug)
    new_cart_total = 0.00
    for beat in cart.beats.all():
        new_cart_total += float(beat.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.beats.count(), 'cart_total_price': cart.cart_total})


def payment(request, beat_slug):
    cart = get_or_create_cart(request)
    beat = Beat.objects.get(slug=beat_slug)
    context = {
        'beat': beat,
    }
    return render(request, 'payment.html', context)
