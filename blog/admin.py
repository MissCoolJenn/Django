from django.contrib import admin
from .models import Post

admin.site.register(Post)
# ^ зарегистрировать в админ панели приложение Post