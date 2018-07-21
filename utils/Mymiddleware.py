from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from users.models import UserModel,UserTicketModel
from django.http import HttpResponseRedirect
from datetime import datetime
import re

class Mymiddle(MiddlewareMixin):

    def process_request(self,request):
        urls = ['/user/login/','/user/register/','para/(\d+)/(\d+)/(\d+)/']
        path = request.path
        for url in urls:
            if re.match(url,path):
                return None
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            if path == '/user/my/':
                return None
            return HttpResponseRedirect(reverse('user:login'))

        user = UserTicketModel.objects.filter(ticket=ticket).first()
        if not user:
            return HttpResponseRedirect(reverse('user:login'))
            # b把user传给页面

        if user.out_time.replace(tzinfo=None) < datetime.now():
            ticket.delete()
            return HttpResponseRedirect(reverse('user:login'))

        request.user = user.user





















