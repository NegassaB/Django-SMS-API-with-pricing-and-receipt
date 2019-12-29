"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

app_name = "ui"

urlpatterns = [
    path('homepage/', views.homepage, name="homepage"),
    path('login/', views.login_request, name="login"),
    path('dashboard/<username>/', views.dashboard, name="dashboard"),
    path('logout_request/', views.logout_request, name="logout"),
    path('register/', views.register_request, name="register"),
    path('ajax/dashboard_update/', views.ajax_dashboard_update, name="ajax_dashboard_update"),
    path('<username>/invoice/', views.invoice_generator, name="invoice_generator"),
]
