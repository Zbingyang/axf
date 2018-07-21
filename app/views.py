from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from app.models import MainWheel, MainNav, MainShop, MainMustBuy, MainShow, CartModel, OrderGoodsModel, OrderModel

from app.models import FoodType,Goods
from utils.free import order_o_num


def Home(request):
    if request.method == 'GET':
        MainWheels = MainWheel.objects.all()
        MainNavs = MainNav.objects.all()
        MainMustBuys = MainMustBuy.objects.all()
        first = MainShop.objects.all()[0]
        second = MainShop.objects.all()[1:5]
        three = MainShop.objects.all()[5:9]
        four = MainShop.objects.all()[9:13]
        MainShows = MainShow.objects.all()

        data = {
            'MainWheels': MainWheels,
            'MainNavs': MainNavs,
            'MainMustBuys': MainMustBuys,
            'first': first,
            'second': second,
            'three': three,
            'four': four,
            'MainShows': MainShows,
        }

        return render(request, 'home/home.html', data)


def Market(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('axf:para',kwargs={'typeid': 104749,
                                                               'cid': 0,
                                                               'sid': 0}))

    # if request.method == 'POST':
    #     user = request.user
    #     goods = request.POST.get('goodsid')
    #     c_num = request.POST.get('c_num')
    #     CartModel.objects.create(user=user,
    #                              goods=goods,
    #                              c_num=c_num)

        
def Para(request, typeid, cid, sid):
    foottypes = FoodType.objects.all()
    goods = Goods.objects.filter(categoryid=typeid)
    if Goods.objects.filter(childcid=cid):
        goods = Goods.objects.filter(childcid=cid)
    childname = FoodType.objects.filter(typeid=typeid).first()
    childname_list = [a.split(':') for a in childname.childtypenames.split('#')]

    if sid == '0':
        pass
    elif sid == '1':
        goods = goods.order_by('productnum')
    elif sid == '2':
        goods = goods.order_by('-price')
    elif sid == '3':
        goods = goods.order_by('price')

    data = {
        'foottypes': foottypes,
        'goods': goods,
        'typeid': typeid,
        'cid': 0,
        'childname_list': childname_list,
        'sid': 0,
    }

    return render(request, 'market/market.html', data)
# ======================购物车===================


def AddToCart(request):
    if request.method == 'POST':
        data = {}
        user = request.user
        good_id = request.POST.get('good_id')
        data['code'] = '1011'
        data['msg'] = '请求失败'
        if user.id:
            cart = CartModel.objects.filter(user=user,goods_id=good_id).first()

            if cart:
                data['msg'] = '请求成功'
                cart.c_num += 1
                data['c_num'] = cart.c_num
                data['code'] = '200'
                cart.save()
                return JsonResponse(data)

            else:
                CartModel.objects.create(user=user,goods_id=good_id)
                data['msg'] = '请求成功'
                data['c_num'] = 1
                data['code'] = '200'
                return JsonResponse(data)

        return JsonResponse(data)



def SubToCart(request):
    if request.method == 'POST':
        data = {}
        data['code'] = '1011'
        data['msg'] = '请求成功'
        user = request.user
        if user.id:
            good_id = request.POST.get('good_id')
            cart = CartModel.objects.filter(goods_id=good_id,user=user).first()
            if cart:
                data['msg'] = '请求成功'
                if cart.c_num == 1:
                    data['code'] = '200'
                    data['c_num'] = 0
                    cart.delete()
                    return JsonResponse(data)
                else:
                    cart.c_num -= 1
                    data['code'] = '200'
                    data['c_num'] = cart.c_num
                    cart.save()
                    return JsonResponse(data)

            else:
                data['msg'] = '请先添加到购物车'
                return JsonResponse(data)
        else:
            data['msg'] = '请先登录'
            return JsonResponse(data)


def ShowNum(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            carts = CartModel.objects.filter(user=user)
            carts_list = []
            if carts:

                for cart in carts:
                    num = {
                        'id': cart.id,
                        'good_id': cart.goods_id,
                        'user_id': user.id,
                        'c_num': cart.c_num,
                    }
                    carts_list.append(num)
                data = {'carts_list': carts_list, 'code': '200'}
                return JsonResponse(data)
            else:

                data = {'code': '1011', 'msg': '请先加入购物车'}
                return JsonResponse(data)
        else:

            data = {'code': '1011', 'msg': '请先登录'}
            return JsonResponse(data)


def Cart(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            carts = CartModel.objects.filter(user=user)
            data = {
                'carts': carts,
            }
            return render(request, 'cart/cart.html', data)



def check(request):
    if request.method == 'POST':
        user = request.user
        cart_id = request.POST.get('cart_id')
        if user.id:
            cart = CartModel.objects.get(pk=cart_id,user=user)
            if cart.is_select:
                cart.is_select = False
                cart.save()
                data = {
                    'code': '200',
                    'is_select': cart.is_select
                }
                return JsonResponse(data)

            else:
                cart.is_select = True
                cart.save()
                data={
                    'code': '200',
                    'is_select': cart.is_select
                }
                return JsonResponse(data)


def totalPrice(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            carts = CartModel.objects.filter(is_select=True,user=user.id)

            total_price = 0
            for cart in carts:
                c_num = CartModel.objects.filter(pk=cart.id)
                good = Goods.objects.filter(pk=cart.goods_id)
                total_price += good.price * c_num.c_num

            total_price = round(total_price, 3)

            total_price = str(total_price)

            data = {
                'code': '200',
                'total': total_price,
            }
            return JsonResponse(data)


def FutureGenerations(request):
    if request.method == 'POST':

        user = request.user
        value = request.POST.get('value')
        if user.id:
            carts = CartModel.objects.all(user=user)
            cart_good_id_list = []
            for cart in carts:
                if value == '√':
                    cart.is_select = False
                    id = {
                        'cart_id':cart.id,
                        'cart_goods_id': cart.goods.id,
                        'is_select': cart.is_select,
                    }
                    cart.save()
                    cart_good_id_list.append(id)

                else:
                    cart.is_select = True
                    id = {
                        'cart_id': cart.id,
                        'cart_goods_id': cart.goods.id,
                        'is_select': cart.is_select,
                    }
                    cart.save()
                    cart_good_id_list.append(id)

            data = {
                'code': '200',
                'cart_good_id_list': cart_good_id_list,
            }
            return JsonResponse(data)


def orderInfo(request):
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        order = OrderModel.objects.get(pk=order_id)
        data = {
            'order': order
        }

        return render(request, 'order/order_info.html', data)

    if request.method == 'POST':
        user = request.user
        if user.id:
            order = order_o_num()
            carts = CartModel.objects.filter(user=user, is_select=True)
            order_id = OrderModel.objects.create(user=user, o_num=order)

            for cart in carts:
                OrderGoodsModel.objects.create(goods_num=cart.c_num, goods=cart.goods, order=order_id)

            carts.delete()

            data = {
                'code': '200',
                'order_id': order_id.id,

            }
            return JsonResponse(data)


# 改变用户下单成功的商品的状态
def changeStatic(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = OrderModel.objects.get(pk=order_id)
        order.o_status = 1
        order.save()
        data = {
            'code': '200',
            'msg': '请求成功',
        }
        return JsonResponse(data)

# 待待收货
def OrderPayed(request):
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(o_status=1, user=user.id)
        data = {
            'orders': orders
        }
        return render(request, 'order/order_list_payed.html', data)


# 代收款
def orderPay(request):
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(o_status=0, user=user.id)
        data = {
            'orders': orders,
        }

        return render(request, 'order/order_list_wait_pay.html', data)




















