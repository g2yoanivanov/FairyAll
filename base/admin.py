from django.contrib import admin
from .models import User, Country, Author, Tale, Message

admin.site.register(User)
admin.site.register(Country)
admin.site.register(Author)
admin.site.register(Tale)
admin.site.register(Message)
