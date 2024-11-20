from django.urls import path
from User import views
urlpatterns = [
    path('register/', views.register_view, name='register_view'),
    path('', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'), 
    path('premium/', views.premium_view, name='premium_view'),
    path('payment/', views.payment_view, name='payment_view'),
    path('update_payment_status/', views.update_payment_status, name='update_payment_status'),
]
