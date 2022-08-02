from django.db import models
import os


def get_upload_path(instance, filename):
    return os.path.join(
        "%s" % instance.system.name, filename)


class ExternSystem(models.Model):
    name = models.CharField(max_length=255)
    system_id = models.IntegerField(blank=True, null=True, default=1)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['system_id']


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
    system = models.ForeignKey(ExternSystem, on_delete=models.CASCADE)
    group = models.ForeignKey(
        FileGroup, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    filename = models.FileField(default='', upload_to=get_upload_path)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Insertion(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, default='')
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    column_from = models.CharField(max_length=255)
    column_to = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class GroupInsertion(models.Model):
    name = models.CharField(max_length=255)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    group = models.ForeignKey(FileGroup, on_delete=models.CASCADE)
    column_from = models.CharField(max_length=255)
    column_to = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class SpecialInsertion(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, default='')
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    column_to = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
