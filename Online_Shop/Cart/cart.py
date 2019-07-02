from decimal import Decimal
from django.conf import settings
from Shop.models import Product


class Cart(object):
	def __init__(self, request):  # Initialize the cart
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}  # Save an empty cart in session
		self.cart = cart

	def add(self, product, quantity=1, update_quantity=False):  # add a product to cart or update quantity
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
		if update_quantity:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id]['quantity'] += quantity
		self.save()

	def save(self):
		self.session.modified = True  # Mark the session as modified to make sure that it get saved

	def remove(self, product):  # Remove a product from the Cart
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):  # Iterate over the items in the cart and get products from database
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		cart = self.cart.copy()
		for product in products:
			cart[str(product.id)]['product'] = product
		for item in cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def __len__(self):  # Count all item in the cart
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):  # Calculate total price of items in cart
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	def clear(self):  # Remove cart from session
		del self.session[settings.CART_SESSION_ID]
		self.save()

