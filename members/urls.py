from django.urls import path
from . import views

urlpatterns=[
    path('admin/create_member/', views.create_member), #POST, {name, discord, github, email, group}
    path('admin/delete_member/', views.delete_member), #POST, {name: }
    path('member/send_email/', views.mail_member), #POST, {'email': }
    path('member/verify_otp/', views.verify_otp), #POST, {'otp': }
    path('member/member_details/', views.member_details), #POST
    path('member/assign_mentor/', views.assign_mentor), #POST {'mentor': , 'mentee': }
    path('member/logout/', views.logout_user), #POST, {} it uses session so no real need
    path('member/select_track/', views.select_track), #POST, {'name': , 'track': }
    path('member/customize/', views.customize), #POST, atleast 1 of {'discord': , 'github': , 'email': , 'pfp': , 'group': , 'year': , 'track': }
    path('member/leaderboard_points/', views.leaderboard_points) #GET 
] 