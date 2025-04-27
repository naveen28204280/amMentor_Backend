from django.urls import path
from . import views

urlpatterns=[
    path('admin/create_member/', views.create_member), #POST, {'name', 'discord','github' , 'email', 'group'}
    path('admin/delete_member/', views.delete_member), #POST, {'name': }
    path('admin/assign_mentor/', views.assign_mentor), #POST {'mentor': , 'mentee': }c
    path('member/member_details/', views.member_details), #POST {"email": or "name"}
    path('member/select_track/', views.select_track), #POST, {'name': , 'track': }
    path('member/customize/', views.customize), #POST, atleast 1 of {'discord': , 'github': , 'email': , 'pfp': , 'group': , 'year': , 'track': }
    path('member/points_leaderboard/', views.leaderboard_points), #GET
    path('member/mentee_details/', views.mentee_details), #POST, {'mentor': ,}
    path('member/mentee_tasks/', views.mentee_tasks) #POST, {'mentor': ,}
]