from datetime import datetime,timedelta

from app.models import OrderModel
from utils.free import Ran
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render
from django.urls import reverse

from users.models import UserTicketModel,UserModel
from django.http import HttpResponseRedirect, HttpResponse


def my(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            orders = OrderModel.objects.filter(user=user.id)
            pay, payed = 0, 0
            for order in orders:
                if order.o_status:
                    payed += 1
                else:
                    pay += 1

            data = {
                'payed': payed,
                'pay': pay,
                'user': user,
            }
            return render(request, 'mine/mine.html', data)
    return render(request, 'mine/mine.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':
        ticket = UserTicketModel()
        username = request.POST.get('username')
        password = request.POST.get('password')

        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.get(username=username)
            if check_password(password,user.password):
                ran = Ran()
                ticket.ticket = ran
                out_time = datetime.now() + timedelta(days=1)
                ticket.out_time = out_time
                res = HttpResponseRedirect(reverse('axf:home'))
                res.set_cookie('ticket', ran,expires=out_time)
                ticket.user = user
                ticket.save()

                return res

            else:
                return HttpResponseRedirect(reverse('user:login'))

        else:
            return HttpResponseRedirect(reverse('user:login'))
    else:
        return HttpResponseRedirect(reverse('user:login'))




def register(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        icon = request.FILES.get('icon')
#  =============存储提交的用户的数据===============
        UserModel.objects.create(username=username,
                                 password=make_password(password),
                                 email=email,
                                 icon=(icon),
                                 )
        return HttpResponseRedirect(reverse('user:login'))

def logout(request):
    if request.method == 'GET':
        username = request.user.username
        user = UserModel.objects.get(username=username)
        UserTicketModel.objects.filter(user=user.id).delete()

        return HttpResponseRedirect(reverse('user:login'))












