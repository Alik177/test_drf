from django.contrib import admin

from .models import *

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Currency)
admin.site.register(Genre)
admin.site.register(Review)

# admin.site.register(Purchase)
# admin.site.register(PurchaseItem)



