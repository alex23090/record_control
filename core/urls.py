from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/worker-signup/', views.worker_register, name='worker-signup'),
    path('accounts/client-signup/', views.client_register, name='client-signup'),

    path('account/', views.account, name='account'),
    path('edit-account', views.editAccount, name='edit-account'),

    path('profile/<str:pk>/', views.profileView, name='profile'),
]