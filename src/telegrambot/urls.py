from django.urls import include, path

from telegrambot import views

urlpatterns = [

     path('verify', views.VerificationView.as_view(), name='update_id_tg')

]
