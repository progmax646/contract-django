from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.

class Contract(models.Model):
    client_id = models.ForeignKey(User, on_delete=models.PROTECT)
    type = models.IntegerField(default='1')
    comment = models.TextField()
    contract_name = models.CharField(max_length=256)
    path = models.CharField(max_length=256, default='0')
    date = models.DateField()
    didox = models.IntegerField(default='0')
    status = models.IntegerField(default='0')
    captcha = models.CharField(max_length=256, default='0')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'

    def __str__(self):
        return self.contract_name

class Role(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название роли')
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True)
    group = models.IntegerField(null=True)
    company_name = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural='Роли'