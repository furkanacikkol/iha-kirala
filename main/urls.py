from django.contrib import admin
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    # Admin Paneli
    path('admin/', admin.site.urls, name='admin-panel'),

    # Ana Sayfa
    path('', views.homepage, name='homepage'),

    # Kullanıcı İşlemleri
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),

    # İHA Listesi İşlemleri
    path('iha-list/', views.iha_list, name='iha-list'),
    path('insert-iha/', views.insert_iha, name='insert-iha'),
    path('edit-iha/<int:iha_id>/', views.edit_iha, name='edit-iha'),
    path('delete-iha/<int:iha_id>/', views.delete_iha, name='delete-iha'),

    # İHA Kiralama İşlemleri
    path('iha-rental-list/', views.iha_rental_list, name='iha-rental-list'),
    path('iha-rental/', views.iha_rental, name='iha-rental'),
    path('rental-list/', views.rental_list, name='rental-list'),

    # Kullanıcı Kiralamaları
    path('user-rentals/', views.user_rentals, name='user-rentals'),
    path('update-rental/', views.update_rental, name='update-rental'),
    path('cancel-rental/', views.cancel_rental, name='cancel-rental'),
]
