from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/', include('users.urls')),
    path('api/', include('cook.urls')),
    path('admin/', admin.site.urls),
]
