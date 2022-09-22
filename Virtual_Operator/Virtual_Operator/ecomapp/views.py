from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth  import login, authenticate
from ecomapp.forms import OrderForm, RegistrationForm, LoginForm
from ecomapp.models import Category, Service, CartItem, Cart, Phone, Order



# Create your views here.
def base_view(request):

    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except Exception:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    categories = Category.objects.all().order_by('name')
    services = Service.objects.all().order_by('price')
    context = {
        'categories': categories,
        'services': services,
        'cart': cart,

    }
    return render(request, 'base.html', context)


def service_view(request, service_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    service = Service.objects.get(slug=service_slug)
    categories = Category.objects.all().order_by('name')
    context = {
        'service': service,
        'categories': categories,
        'cart': cart,
    }
    return render(request, 'service.html', context)


def category_view(request, category_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all().order_by('name')
    services_of_category = category.service_set.all().order_by('price')
    context = {
        'category': category,
        'services_of_category': services_of_category,
        'categories':  categories,
        'cart': cart
    }
    return render(request, 'category.html', context)


def cart_view(request):
    phones = Phone.objects.filter(user=request.user).order_by('phone_number')
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except Exception:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    categories = Category.objects.all().order_by('name')
    context = {
        'cart': cart,
        'phones': phones,
        'categories': categories
    }
    return render(request, 'cart.html', context)


# Добавление в корзину
def add_to_cart_view(request):

    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except Exception:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    service_slug = request.GET.get("service_slug")
    service = Service.objects.get(slug=service_slug)
    cart.add_to_cart(service.slug)

    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


# Удаление из корзины
def remove_from_cart_view(request):

    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except Exception:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    service_slug = request.GET.get('service_slug')
    service = Service.objects.get(slug=service_slug)
    cart.remove_from_cart(service.slug)

    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def add_phone_to_cart(request):

    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except Exception:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    phone_number = request.GET.get('phone_number')
    item_id = request.GET.get('item_id')

    cart_item = CartItem.objects.get(id=int(item_id))
    cart_item.phone = phone_number
    cart_item.save()

    return JsonResponse({'cart_total': cart.items.count(), 'phone_number': cart_item.phone})


def checkout_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except Exception:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    categories = Category.objects.all().order_by('name')
    context = {
        'cart': cart,
        'categories': categories
    }
    return render(request, 'checkout.html', context)


def order_create_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except Exception:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = OrderForm(request.POST or None)
    categories = Category.objects.all().order_by('name')
    context = {
        'form': form,
        'cart': cart,
        'categories': categories
    }
    return render(request, 'order.html', context)


def make_order_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except Exception:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    categories = Category.objects.all().order_by('name')
    form = OrderForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        third_name = form.cleaned_data['third_name']
        order_phone = form.cleaned_data['order_phone']
        buying_type = form.cleaned_data['buying_type']
        address = form.cleaned_data['address']
        new_order = Order.objects.create(
            user=request.user,
            items=cart,
            total=cart.cart_total,
            first_name=name,
            last_name=last_name,
            third_name=third_name,
            order_phone=order_phone,
            address=address,
            buying_type=buying_type
        )
        del request.session['cart_id']
        del request.session['total']
        return HttpResponseRedirect(reverse('thank_you'))
    return render(request, 'order.html', {'categories': categories})


def account_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    order = Order.objects.filter(user=request.user).order_by('-date')
    categories = Category.objects.all().order_by('name')

    context = {
        'order': order,
        'categories': categories,
        'cart': cart
    }
    return render(request, 'account.html', context)



def registration_view(request):
    form = RegistrationForm(request.POST or None)
    categories = Category.objects.all().order_by('name')
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'registration.html', context)



def login_view(request):
    form = LoginForm(request.POST or None)
    categories = Category.objects.all().order_by('name')
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'login.html', context)