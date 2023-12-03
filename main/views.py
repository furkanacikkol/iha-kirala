from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import api_view
from rest_framework import viewsets

from .models import IHA, Rental
from .forms import NewUserForm
from .serializers import IHASerializer, RentalSerializer



class IHAViewSet(viewsets.ModelViewSet):
    queryset = IHA.objects.all()
    serializer_class = IHASerializer

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer


# Admin kontrolü için yardımcı fonksiyon
def is_admin(user):
    return user.is_superuser

# Kayıt olma işlemi
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Kayıt olma başarılı." )
            return redirect("/")
        messages.error(request, "Başarısız kayıt olma. Bilgiler geçersiz.")
    form = NewUserForm()
    return render (request=request, template_name="main/register.html", context={"register_form":form})

# Giriş yapma işlemi
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"{username} olarak giriş yaptınız.")
                return redirect("/")
            else:
                messages.error(request,"Yanlış kullancı adı ve şifre.")
        else:
            messages.error(request,"Yanlış kullancı adı ve şifre.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form":form})

# Ana sayfa
def homepage(request):
    all_ihas = IHA.objects.all()
    context = {'all_ihas': all_ihas}
    return render(request, 'main/homepage.html', context)

# Çıkış yapma işlemi
def logout_request(request):
    logout(request)
    messages.info(request, "Başarıyla çıkış yaptınız.") 
    return redirect("/")

# İHA kiralama listesi
def iha_rental_list(request):
    all_ihas = IHA.objects.all()
    return render(request, 'main/iha_rental.html', {'all_ihas': all_ihas})

# İHA kiralama işlemi
@require_POST
def iha_rental(request):
    iha_id = request.POST.get('iha_id')
    iha = get_object_or_404(IHA, id=iha_id)

    start_datetime = timezone.now()
    end_datetime = start_datetime + timezone.timedelta(days=1)

    user = request.user

    rental = Rental.objects.create(
        iha=iha,
        user=user,
        start_datetime=start_datetime,
        end_datetime=end_datetime
    )
    messages.success(request, 'Kiralama başarıyla güncellendi.')

    return HttpResponse("İHA kiralama başarılı!") 

# İHA kiralama güncelleme işlemi
def update_rental(request):
    rental_id = request.POST.get('rental_id')
    end_date = request.POST.get('end_date')

    rental = get_object_or_404(Rental, id=rental_id)

    rental.end_datetime = timezone.datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S')

    rental.save()

    return HttpResponse("İHA bilgilerini güncelleme başarılı!") 

# İHA kiralama iptali
def cancel_rental(request):
    print("Kiralama İptali Görünümüne Ulaşıldı")
    rental_id = request.POST.get('rental_id')
    rental = get_object_or_404(Rental, pk=rental_id)
    rental.delete()
    messages.success(request, 'Kiralama başarıyla iptal edildi.')
    
    return HttpResponse("İHA kiralama başarılıyla iptal edildi.") 

# İHA listesi
def iha_list(request):
    all_ihas = IHA.objects.all()
    return render(request, 'main/iha_list.html', {'all_ihas': all_ihas})

# İHA ekleme işlemi
@user_passes_test(is_admin)
def insert_iha(request):
    if request.method == 'POST':
        # POST isteği geldiğinde form verilerini al
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        weight = request.POST.get('weight')
        range_value = request.POST.get('range')
        payload_capacity = request.POST.get('payload_capacity')
        max_speed = request.POST.get('max_speed')
        category = request.POST.get('category')

        # Veritabanına yeni IHA ekle
        iha = IHA.objects.create(brand=brand, model=model, weight=weight, category=category, range=range_value,payload_capacity=payload_capacity,max_speed=max_speed)

        return HttpResponse("İHA ekleme başarılı!") 

# İHA güncelleme işlemi
@user_passes_test(is_admin)
def edit_iha(request, iha_id):
    iha = get_object_or_404(IHA, id=iha_id)

    if request.method == 'POST':
        # POST isteği geldiğinde form verilerini al
        iha.brand = request.POST.get('brand')
        iha.model = request.POST.get('model')
        iha.weight = request.POST.get('weight')
        iha.range = request.POST.get('range')
        iha.payload_capacity = request.POST.get('payload_capacity')
        iha.max_speed = request.POST.get('max_speed')
        iha.category = request.POST.get('category')
        iha.save()
        messages.success(request, 'İHA başarıyla güncellendi.') 

        return redirect('iha-list') 

    return render(request, 'main/edit_iha.html', {'iha': iha})

# İHA silme işlemi
@user_passes_test(is_admin)
def delete_iha(request, iha_id):
    iha = get_object_or_404(IHA, id=iha_id)
    iha.delete()
    messages.success(request, 'İHA başarıyla silindi.')
    return redirect('iha-list')

# Kullanıcı kiralama listesi
def user_rentals(request):
    user_rentals = Rental.objects.filter(user=request.user)
    return render(request, 'main/user_rentals.html', {'user_rentals': user_rentals})

# Admin kiralama listesi
@user_passes_test(is_admin)
def rental_list(request):
    user_rentals = Rental.objects.all()
    return render(request, 'main/rental_list.html', {'user_rentals': user_rentals})
