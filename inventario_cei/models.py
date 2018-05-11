from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=200)
    mail = models.EmailField()
    photo = models.FileField()


class Admin(Profile):
    pass


class Client(Profile):
    ENABLE = (
        ('si', 'Habilitado'),
        ('no', 'No Habilitado')
    )
    enable = models.CharField(max_length=2, choices=ENABLE)


class Reserve(models.Model):
    start = models.DateTimeField()
    finish = models.DateTimeField()
    STATES = (
        ('a', 'Aceptada'),
        ('r', 'Rechazada'),
        ('p', 'Pendiente')
    )
    state = models.CharField(max_length=1, choices=STATES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Item(models.Model):
    name = models.CharField(max_length=200)
    image = models.FileField()
    description = models.TextField()
    reserves = models.SET(models.ForeignKey(Reserve, on_delete=models.CASCADE))


class Object(Item):
    CONDITIONS = (
        ('d', 'Disponible'),
        ('p', 'En Préstamo'),
        ('r', 'En Reparación'),
        ('l', 'Perdido')
    )
    condition = models.CharField(max_length=1, choices=CONDITIONS)


class Space(Item):
    CONDITIONS = (
        ('d', 'Disponible'),
        ('p', 'En Préstamo'),
        ('r', 'En Reparación')
    )
    condition = models.CharField(max_length=1, choices=CONDITIONS)
    capacity = models.IntegerField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
