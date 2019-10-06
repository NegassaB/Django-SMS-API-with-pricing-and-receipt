"""api URL Configuration

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
from django.contrib import admin
from django.urls import path, include, re_path
from commons.views import homepage

urlpatterns = [
    # for the homepage
    path('', homepage, name="homepage" ),
    # for the admin page
    path('admin/', admin.site.urls),
    # for the commons app
    path('commons/', include('commons.urls')),
    # for the notification app
    path('notification/', include('notification.urls'))
    # Read the below N.B.
    # re_path(r'^api-auth/', include('rest_framework.urls')),
]

"""
the url(r'^api-auth/', include('rest_framework.urls')) was directly copied from the official django rest framework website.
It stated that this will handle the necessary login and logout issues pertaining to the api. So it was copied here to test.
During testing it request that CSRF token be set.
"""
