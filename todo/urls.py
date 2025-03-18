from django.urls import path, include
from . import views
from django.contrib import admin

app_name = "todo"

urlpatterns=[
    path("admin/", admin.site.urls),
    path("login/", views.login , name="login"),
    path("signup/" , views.signup , name= "signup" ),
    path("<str:user>/" , views.list , name= "list" ),
    path("<str:user>/add-item/" , views.add_item , name= "add-item" ),
    path('toggle_status/<int:item_id>/', views.toggle_status, name='toggle_status'),

    # path("api/task-list/", views.taskList, name="task-list"),
    # path("api/task-detail/<int:pk>/", views.taskDetail, name="task-detail"),
    # path("api/task-create/", views.taskCreate, name="task-create"),
    # path("api/task-update/<int:pk>/", views.taskUpdate, name="task-update"),
    # path("api/task-delete/<int:pk>/", views.taskDelete, name="task-delete"),

    path("api/item-list/", views.ItemList.as_view(), name="item-list"),
    path("api/item-detail/<int:pk>/", views.ItemDetail.as_view(), name="item-detail"),
]
