from django.urls import path
from . import views
from django.contrib import admin


app_name = "todo"

urlpatterns=[
    path("admin/", admin.site.urls),
    path("login/", views.login , name="login"),
    path("signup/" , views.signup , name= "signup" ),
    path("<str:username>/" , views.list , name= "list" ),
    path("<str:username>/add-item/" , views.add_item , name= "add-item" ),
    path('toggle_status/<int:item_id>/', views.toggle_status, name='toggle_status'),
]