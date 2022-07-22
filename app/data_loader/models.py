from django.db import models


class ExternSystem(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Table(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class File(models.Model):
    name = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    system = models.ForeignKey(ExternSystem, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Sustitution(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    column_from = models.CharField(max_length=255)
    column_to = models.CharField(max_length=255)
