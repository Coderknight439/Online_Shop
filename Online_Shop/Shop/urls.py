from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'shop'

urlpatterns = [
	path('', views.product_list, name='product_list'),
	url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
	path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
