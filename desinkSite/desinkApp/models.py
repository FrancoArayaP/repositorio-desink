from django.db import models

class Disenador(models.Model):
    id_disenador = models.AutoField(primary_key=True)
    email = models.CharField(max_length=150, unique=True)
    pass_hash = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

