
from django.conf.urls import  url
from app import views


urlpatterns = [
    # 主页
    url(r'^home/', views.Home, name='home'),
    # 中间页面，传入参数，跳转到闪购页面
    url(r'^market/', views.Market, name='market'),
    # 闪购页面
    url(r'^para/(?P<typeid>\d+)/(?P<cid>\d+)/(?P<sid>\d+)/', views.Para, name='para'),
    # 购物车

    #添加商品
    url(r'^addtocart/', views.AddToCart, name='addtocart'),
    # 删除商品
    url(r'^subtocart/', views.SubToCart, name='subtocart'),
    # 展示选中的商品数量
    url(r'^shownum/', views.ShowNum, name='shownum'),
    # 购物车
    url(r'^cart/', views.Cart, name='cart'),
    # 购物车取消和选中
    url(r'^check/', views.check, name='check'),
    # 算出商品的总价
    url(r'^totalPrice/', views.totalPrice, name='totalPrice'),
    # 全选按钮
    url(r'^FutureGenerations/', views.FutureGenerations, name='FutureGenerations'),
    # 下单按钮
    url(r'^orderInfo/', views.orderInfo, name='orderInfo'),
    #改变下单成功的商品的状态
    url(r'changeStatic/', views.changeStatic, name='changeStatic'),
    #已经付款
    url(r'^orderpayed/', views.OrderPayed, name='orderpayed'),
    # 代收款
    url(r'^orderpay/', views.orderPay, name='orderpay'),



]













