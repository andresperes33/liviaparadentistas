from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bot_messages.urls')), # Atualizado para o novo nome!
    path('', include('subscriptions.urls')),
]
