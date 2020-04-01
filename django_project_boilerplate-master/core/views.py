from django.shortcuts import render, get_object_or_404
from .models import Item, Order, OrderItem
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm


def products(request):
    context = {
        'item': Item.objects.all()
    }
    return render(request, "products.html", context)


class CheckoutView(View):
    def get(self, request, * args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(request, "checkout.html", context)

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if forms.is_valid():
            print("Форма валидна")
            return redirect("core:checkout")


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "order_summary.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "У вас нет активных заказов")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,
                                                          user=request.user,
                                                          ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(
                request, "Количество этого товара в корзине было обновлено.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Этот товар добавлен к вам в корзину.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Этот товар добавлен к вам в корзину.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,
                                                  user=request.user,
                                                  ordered=False)[0]
            order_item.quantity = 1
            order_item.save()
            order.items.remove(order_item)
            messages.info(request, "Этот товар удален с вашей  корзины.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "Этот товар не в вашей корзине.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "У вас нет активного заказа.")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,
                                                  user=request.user,
                                                  ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "Количество этого товара было обновлено")
            return redirect("core:order-summary")
        else:
            messages.info(request, "Этот товар не в вашей корзине.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "У вас нет активного заказа.")
        return redirect("core:product", slug=slug)
