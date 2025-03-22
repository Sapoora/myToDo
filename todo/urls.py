from django.urls import path
from todo import views
from django.contrib import admin

app_name = "todo"

urlpatterns=[
    path("admin/", admin.site.urls),

    path("", views.init , name= "init" ),

    path("signup/", views.signup_user , name="signup"),
    path("login/" , views.login_user , name= "login" ),
    path("logout/" , views.logout_user , name= "logout" ),

    path("<str:user>/" , views.list , name= "list" ),
    path("<str:user>/add-item/" , views.add_item , name= "add-item" ),
    path('toggle_status/<int:item_id>/', views.toggle_status, name='toggle_status'),

    path("api/item-list/", views.ItemList.as_view(), name="item-list"),
    path("api/item-detail/<int:pk>/", views.ItemDetail.as_view(), name="item-detail"),
]
