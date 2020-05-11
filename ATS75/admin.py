from django.contrib import admin

from .models import Student,Subject,TTCell,ARCell

# Register your models here.

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(TTCell)
admin.site.register(ARCell)