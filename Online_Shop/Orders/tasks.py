from celery import task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings

@task
def order_created(order_id):  # Task to send e-mail when order is successfully created
	order = Order.objects.get(id=order_id)
	subject = 'Order No. {}'.format(order.id)
	message = 'Dear {}, \n \n You have successfully placed an order. Your order id is {}'.format(order.first_name, order.id)
	mail_sent = send_mail(subject, message, 'mahadirony.rony@gmail.com', [order.email], fail_silently=False)
	return mail_sent



