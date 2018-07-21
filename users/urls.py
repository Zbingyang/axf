from django.conf.urls import  url
from users import views
urlpatterns = [
    url(r'^my/', views.my, name='my'),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^logout/',views.logout, name='logout'),

]
