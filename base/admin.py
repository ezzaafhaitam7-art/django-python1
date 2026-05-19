from django.contrib import admin
from .models import Bien, ImageBien

class ImageBienInline(admin.TabularInline):
    model = ImageBien
    extra = 1
    max_num = 10   

class BienAdmin(admin.ModelAdmin):
    inlines = [ImageBienInline]

admin.site.register(Bien, BienAdmin)
admin.site.register(ImageBien)
# Register your models here.
