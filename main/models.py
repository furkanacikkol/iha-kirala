from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class IHA(models.Model):
    # İHA'nın özellikleri
    brand = models.CharField(max_length=255, verbose_name="Marka")
    model = models.CharField(max_length=255, verbose_name="Model")
    weight = models.FloatField(verbose_name="Ağırlık")
    category = models.CharField(max_length=255, verbose_name="Kategori")
    payload_capacity = models.FloatField(verbose_name="Yük Taşıma Kapasitesi")
    range = models.FloatField(verbose_name="Uçuş Menzili")
    max_speed = models.FloatField(verbose_name="Maksimum Hız")

    def __str__(self):
        return f"{self.brand} - {self.model}"

class Rental(models.Model):
    # Kiralama özellikleri
    iha = models.ForeignKey(IHA, on_delete=models.CASCADE, verbose_name="Kiralanan İHA")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kiralayan Üye")
    start_datetime = models.DateTimeField(verbose_name="Başlangıç Tarihi ve Saati")
    end_datetime = models.DateTimeField(verbose_name="Bitiş Tarihi ve Saati")

    #Toplam sürenin hesaplanması
    def get_total_duration(self):
        duration = self.end_datetime - self.start_datetime
        return duration.total_seconds() // 3600 

    def __str__(self):
        return f"{self.iha.brand} - {self.start_datetime} to {self.end_datetime}"