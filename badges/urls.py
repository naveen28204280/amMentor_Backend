from django.urls import path
from . import views

urlpatterns=[
    path('admin/create_badge/', views.make_badge), #POST, {'badge': , 'icon': }
    path('member/delete_badge/', views.delete_badge), #POST, {'badge': }
    path('member/assign_badge/', views.assign_badge), #POST, {"badge": , "member": }
    path('member/badges_earned/', views.badges_earned) #POST {'name': }
]