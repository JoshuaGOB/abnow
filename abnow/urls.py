"""abolition_now URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from . import views

app_name = 'abnow'

urlpatterns = [
    path('abnow/', include('abnow.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('upload_image/', views.upload_image_view, name='upload_image'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # new
    path('view_image/<int:image_id>/', views.view_image, name='view_image'),
    path('edit_image/<int:image_id>/', views.edit_image, name='edit_image'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('create_code/', views.create_code_view, name='create_code'),
    path('create_code_category/', views.create_code_category_view, name='create_code_category'),
    path('create_sub_code', views.create_sub_code_view, name='create_sub_code'),
    path('create_code_category/', views.create_code_category_view, name='create_code_category'),
    path('create_sub_code/', views.create_sub_code_view, name='create_sub_code'),
    path('view_code_category/<int:code_category_id>/', views.view_code_category, name='view_code_category'),
    path('view_sub_code/<int:sub_code_id>/', views.view_sub_code, name='view_sub_code'),
    path('view_code/<int:code_id>/', views.view_code, name='view_code'),
    path('edit_code/<int:code_id>/', views.edit_code, name='edit_code'),
    path('create_code_category/', views.create_code_category_view, name='create_code_category'),
    path('edit_code_category/<int:code_category_id>/', views.edit_code_category, name='edit_code_category'),
    path('create_sub_code/', views.create_sub_code_view, name='create_sub_code'),
    path('image_list/', views.image_list_view, name='image_list'),
    path('search/', views.search_view, name='search'),
]