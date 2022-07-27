from django.db import models


class ExternSystem(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Table(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class FileGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class File(models.Model):
    name = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    system = models.ForeignKey(ExternSystem, on_delete=models.CASCADE)
    group = models.ForeignKey(
        FileGroup, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Insertion(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    column_from = models.CharField(max_length=255)
    column_to = models.CharField(max_length=255)


class SpecialInsertion(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    column_to = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
