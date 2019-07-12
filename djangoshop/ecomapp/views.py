from django.shortcuts import render
from random import sample
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.http import JsonResponse, HttpResponseRedirect
from ecomapp.forms import (
    OrderForm,
    RegForm,
    LoginForm,
    ProductFilterForm,
)
from ecomapp.models import (
    Category,
    Product,
    CartItem,
    Cart,
    Order,
)


# Create your views here.
def base_view(request):
    try:
        cart_id = request.session["cart_id"]
        cart = Cart.objects.get(id=cart_id)
        request.session["total"] = cart.items.count()
    except KeyError:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = ProductFilterForm(request.GET)
    categories = Category.objects.all()

    if form.is_valid():
        products = Product.objects.all()
        if form.cleaned_data["min_price"]:
            products = products.filter(price__gte=form.cleaned_data["min_price"])
        if form.cleaned_data["max_price"]:
            products = products.filter(price__lte=form.cleaned_data["max_price"])
        context = {
            "categories": categories,
            "products": products,
            "cart": cart,
            "form": form,
        }

        if form.cleaned_data["min_price"] is None and form.cleaned_data["max_price"] is None:
            n_products = Product.objects.all().count()
            if n_products >= 6:
                s_products = sample(range(1, n_products), 6)
                products = Product.objects.filter(id__in=s_products)
            else:
                products = Product.objects.all()
            context = {
                "categories": categories,
                "products": products,
                "cart": cart,
                "form": form,
            }

            return render(request, "base.html", context)
        else:

            return render(request, "search.html", context)


def product_view(request, product_slug):
    try:
        cart_id = request.session["cart_id"]
        cart = Cart.objects.get(id=cart_id)
        request.session["total"] = cart.items.count()
    except KeyError:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)

    product = Product.objects.get(slug=product_slug)
    categories = Category.objects.all()
    context = {
        "product": product,
        "categories": categories,
        "cart": cart,
    }
    return render(request, "product.html", context)


def category_view(request, category_slug):
    categories = Category.objects.all()
    category = Category.objects.get(slug=category_slug)
    products_of_category = Product.objects.filter(category=category)
    context = {
        "category": category,
        "products_of_category": products_of_category,
        "categories": categories
    }
    return render(request, "category.html", context)


def cart_view(request):
    try:
        cart_id = request.session["cart_id"]
        cart = Cart.objects.get(id=cart_id)
        request.session["total"] = cart.items.count()
    except KeyError:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    context = {
        "cart": cart,
        "categories": categories,
    }
    return render(request, "cart.html", context)


def add_to_cart_view(request):
    try:
        cart_id = request.session["cart_id"]
        cart = Cart.objects.get(id=cart_id)
        request.session["total"] = cart.items.count()
    except KeyError:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get("product_slug")
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({"cart_total": cart.items.count(),
                         "cart_total_price": cart.cart_total,
                         })


def remove_from_cart_view(request):
    try:
        cart_id = request.session["cart_id"]
        cart = Cart.objects.get(id=cart_id)
        request.session["total"] = cart.items.count()
    except KeyError:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get("product_slug")
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({"cart_total": cart.items.count(),
                         "cart_total_price": cart.cart_total,
                         })


def change_item_qty(request):
    try:
        cart_id = request.session["cart_id"]
        cart = Cart.objects.get(id=cart_id)
        request.session["total"] = cart.items.count()
    except KeyError:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
    qty = request.GET.get("qty")
    item_id = request.GET.get("item_id")
    cart.change_qty(qty, item_id)
    cart_item = CartItem.objects.get(id=int(item_id))
    return JsonResponse({"cart_total": cart.items.count(),
                         "item_total": cart_item.item_total,
                         "cart_total_price": cart.cart_total,
                         })


def checkout_view(request):
    try:
        cart_id = request.session["cart_id"]
        cart = Cart.objects.get(id=cart_id)
        request.session["total"] = cart.items.count()
    except KeyError:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    context = {
        "cart": cart,
        "categories": categories,
    }
    return render(request, "checkout.html", context)


def order_create_view(request):
    try:
        cart_id = request.session["cart_id"]
        cart = Cart.objects.get(id=cart_id)
        request.session["total"] = cart.items.count()
    except KeyError:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    form = OrderForm(request.POST or None)
    context = {
        "form": form,
        "cart": cart,
        "categories": categories,
    }
    return render(request, "order.html", context)


def make_order_view(request):
    try:
        cart_id = request.session["cart_id"]
        cart = Cart.objects.get(id=cart_id)
        request.session["total"] = cart.items.count()
    except KeyError:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    form = OrderForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data["name"]
        last_name = form.cleaned_data["last_name"]
        phone = form.cleaned_data["phone"]
        buying_type = form.cleaned_data["buying_type"]
        address = form.cleaned_data["address"]
        comments = form.cleaned_data["comments"]
        mew_oder = Order.objects.create(
            user=request.user,
            items=cart,
            total=cart.cart_total,
            first_name=name,
            last_name=last_name,
            phone=phone,
            address=address,
            buying_type=buying_type,
            comments=comments
        )
        del request.session["cart_id"]
        del request.session["total"]
        return HttpResponseRedirect(reverse('thank_you'))
    return render(request, "order.html", {"categories": categories})


def account_view(request):
    if str(request.user) == "Grey":
        order = Order.objects.order_by("-id")
        categories = Category.objects.all()
        context = {
            "order": order,
            "categories": categories
        }
        return render(request, "orders.html", context)
    order = Order.objects.filter(user=request.user).order_by("-id")
    categories = Category.objects.all()
    context = {
        "order": order,
        "categories": categories
    }

    return render(request, "account.html", context)


def registration_view(request):
    form = RegForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        email = form.cleaned_data["email"]
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse("base"))
    context = {
        "form": form,
        "categories": categories,
    }
    return render(request, "registration.html", context)


def login_view(request):
    categories = Category.objects.all()
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse("base"))
    context = {
        "form": form,
        "categories": categories,
    }
    return render(request, "login.html", context)
