from django.db import models
from django.contrib.auth.models import User


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
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(default='')

    class Meta:
        verbose_name_plural = "Items"

    def __str__(self):
        return self.name


class Object(models.Model):
    item = models.OneToOneField(Item, null=True, on_delete=models.CASCADE)
    image = models.FileField(upload_to='inventario_cei/static/img/items/objects')
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
    image = models.FileField(upload_to='inventario_cei/static/img/items/spaces')
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