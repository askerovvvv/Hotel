from django.contrib import admin

from applications.product.models import *


admin.site.register(Category)
admin.site.register(Reservation)
admin.site.register(HotelsIk)


class ImageInAdmin(admin.TabularInline):
    model = ElementImage
    fields = ('image', )
    max_num = 5


@admin.register(Element)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInAdmin
    ]
