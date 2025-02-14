from .cart import Cart

#create context processor so out cart can work on all site
def cart(request):
    return {'cart': Cart(request)}