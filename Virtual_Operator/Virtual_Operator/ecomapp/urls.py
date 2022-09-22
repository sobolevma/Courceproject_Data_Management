from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

from ecomapp.views import (
  base_view,
  category_view,
  service_view,
  cart_view,
  add_to_cart_view,
  remove_from_cart_view,
  add_phone_to_cart,
  checkout_view,
  order_create_view,
  make_order_view,
  account_view,
  registration_view,
  login_view
)


urlpatterns = [
  url(r'^category/(?P<category_slug>[.\w]+)/$', category_view, name='category_detail'),
  url(r'^service/(?P<service_slug>[.\w]+)/$', service_view, name='service_detail'),
  url(r'^add to cart/$', add_to_cart_view, name='add_to_cart'),
  url(r'^remove from cart/$', remove_from_cart_view, name='remove_from_cart'),
  url(r'^add phone to cart/$', add_phone_to_cart, name='add_phone_to_cart'),
  url(r'^My_Cart/$', cart_view, name='cart'),
  url(r'^Checkout_of_cart/$', checkout_view, name='checkout'),
  url(r'^Order/$', order_create_view, name='create_order'),
  url(r'^make order/$', make_order_view, name='make_order'),
  url(r'^Thank_you_for_order/$', TemplateView.as_view(template_name='thank_you.html'), name='thank_you'),
  url(r'^Personal_account/$', account_view, name='account'),
  url(r'^Registration/$', registration_view, name='registration'),
  url(r'^login/$', login_view, name='login'),
  url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('base')), name='logout'),
  url(r'^IMIAREK/$', base_view, name='base'),
  ]

