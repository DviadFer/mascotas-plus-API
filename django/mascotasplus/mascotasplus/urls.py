"""mascotasplus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from restapi import endpoints_user, endpoints_walks, endpoint_walk_by_id, endpoints_companions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest/version/1/users', endpoints_user.register),
    path('rest/version/1/sessions', endpoints_user.login),
    path('rest/version/1/walks', endpoints_walks.request_walk),
    path('rest/version/1/walks/<int:ida>', endpoint_walk_by_id.get),
    path('rest/version/1/walks/<int:id>/companions', endpoints_companions.request_companion),
    path('rest/version/1/walks/<int:id>/companions/<int:request_id>', endpoints_companions.accept_request)
]
