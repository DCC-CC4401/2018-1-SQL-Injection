from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=200)
    mail = models.EmailField()
    photo = models.FileField(upload_to='inventario_cei/static/img/profile_pictures')


class Admin(Profile):
    class Meta:
        verbose_name_plural = "Administradores"


class Client(Profile):
    ENABLE = (
        ('si', 'Habilitado'),
        ('no', 'No Habilitado')
    )
    enable = models.CharField(max_length=2, choices=ENABLE)

    class Meta:
        verbose_name_plural = "Clientes"


class Item(models.Model):
    name = models.CharField(max_length=200)
    # image = models.FileField(upload_to='inventario_cei/static/img/items')
    description = models.TextField(default='')

    # reserves = models.SET(models.ForeignKey(Reserve, default=None, on_delete=models.CASCADE))
    class Meta:
        #     abstract = True
        verbose_name_plural = "Items"


class Object(models.Model):
    item = models.OneToOneField(Item, null=True, on_delete=models.CASCADE)
    image = models.FileField(upload_to='inventario_cei/static/img/items/objects')  # Overriding parent class attribute
    CONDITIONS = (
        ('d', 'Disponible'),
        ('p', 'En Préstamo'),
        ('r', 'En Reparación'),
        ('l', 'Perdido')
    )
    condition = models.CharField(max_length=1, choices=CONDITIONS)

    class Meta:
        verbose_name_plural = "Objetos"


class Space(models.Model):
    item = models.OneToOneField(Item, null=True, on_delete=models.CASCADE)
    image = models.FileField(upload_to='inventario_cei/static/img/items/spaces')  # Overriding parent class attribute
    CONDITIONS = (
        ('d', 'Disponible'),
        ('p', 'En Préstamo'),
        ('r', 'En Reparación')
    )
    condition = models.CharField(max_length=1, choices=CONDITIONS)
    capacity = models.IntegerField()

    class Meta:
        verbose_name_plural = "Espacios"


class Reserve(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    start = models.DateTimeField()
    finish = models.DateTimeField()
    STATES = (
        ('a', 'Aceptada'),
        ('r', 'Rechazada'),
        ('p', 'Pendiente')
    )
    state = models.CharField(max_length=1, choices=STATES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE)

    # object = models.ForeignKey(Object, null=True, on_delete=models.CASCADE)
    # space = models.ForeignKey(Space, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Reservas"

# TODO: deprecated, problem with primary key 'rut'
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()