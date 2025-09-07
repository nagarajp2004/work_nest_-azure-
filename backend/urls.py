from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # This path directs traffic to the built-in Django admin site.
    path('admin/', admin.site.urls),
    
    # This path is the crucial connection to your API. It tells Django that
    # any URL that starts with 'api/' should be handed over to the urls.py
    # file located inside your 'api' application.
    path('api/', include('api.urls')),
]

