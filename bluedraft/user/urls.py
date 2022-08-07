from django.urls import path, include

app_name = 'user'

urlpatterns = [
    # USERS
    path('accounts/', include('django.contrib.auth.urls')),
]
