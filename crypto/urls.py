from django.urls import path, re_path, include

from crypto import views

app_name = 'crypto'

urlpatterns = [
	path('', views.landing, name='dashboard'),
]
