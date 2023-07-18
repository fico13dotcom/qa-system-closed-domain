
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('consultas/', include('consultas.urls')),
    path('login/', include('login.urls')),
    # path('login/', )
]