from django.db import models
from django.contrib.auth.models import User

class ATS(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.name} {self.location}'

class OLT(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    ats = models.ForeignKey(ATS, related_name='olt',on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f'{self.ip} {self.model}'

class ONT(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    serial = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    port = models.IntegerField()
    pon_id = models.IntegerField()
    personal = models.CharField(max_length=100,null=True)
    physic_personal = models.CharField(max_length=100,null=True,blank=True)
    olt = models.ForeignKey(OLT, related_name='ont',on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
        return f'{self.serial} {self.model}'

class RSSI(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    rx = models.FloatField()
    tx = models.FloatField()
    ont = models.ForeignKey(ONT, related_name='rssi',on_delete=models.CASCADE,null=True, blank=True)

class OPERATIONS(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    author_ip = models.CharField(max_length=100,null=True)
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=100)
    ch_user = models.BooleanField(null=True)
    ch_login = models.BooleanField(null=True)
    ch_password = models.BooleanField(null=True)
    ch_profile = models.BooleanField(null=True)
    ch_reconf = models.BooleanField(null=True)
    ch_saved = models.BooleanField(null=True)
    ont = models.ForeignKey(ONT, related_name='ont',on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
        return f'{self.author} {self.status}'