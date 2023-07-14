# models.py
from django.db import models
from django.contrib.auth.models import User

class CodeCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Code(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(CodeCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class SubCode(models.Model):
    name = models.CharField(max_length=255)
    code = models.ForeignKey(Code, related_name='sub_codes', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code.name} - {self.name}"


class Image(models.Model):
    name = models.CharField(max_length=255, unique=True )
    filename = models.CharField(max_length=255)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')
    codes = models.ManyToManyField(Code, related_name='images', blank=True)
    sub_codes = models.ManyToManyField(SubCode, blank=True)

    def __str__(self):
        return self.filename