from django.contrib import admin
from .models import CodeCategory, Code, SubCode, Image

admin.site.register(CodeCategory)
admin.site.register(Code)
admin.site.register(SubCode)
admin.site.register(Image)
