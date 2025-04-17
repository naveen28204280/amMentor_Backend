from django.urls import path
from . import views

urlpatterns=[
    path('admin/create_track/', views.create_track), # POST, {'track': }
    path('admin/delete_track/', views.delete_track), #POST, {'track': }
    path('admin/create_task/', views.create_task), #POST, {'task_name': ,'task_num': , 'task_description': , 'points': , 'deadline': , 'track': ,}
    path('admin/delete_task/', views.delete_task), #POST, {'task_name': , 'task_num': ,'track':  }
    path('member/display_tracks/', views.display_tracks), #GET
    path('member/select_track/', views.select_track), #POST {'member': , "track": }
    path('member/display_tasks/', views.display_all_tasks), #POST {'member': , 'track': }
    path('member/task_details/', views.display_task_details), #POST {'task_name': , 'track': , 'task_num': , 'member': }
    path('member/start_task/', views.start_task), #POST,  {'task_name': , 'task_num': , 'track': , 'member': }
    path('mentor/pause_task/', views.pause_task), #POST, {'mentor': , 'mentee': , 'task_name': , 'task_num': , 'track': }
    path('mentor/resume_task/', views.resume_task), #POST, {'mentor': , 'mentee': , 'task_name': , 'task_num': , 'track': }
    path('member/submit_task/', views.mentee_submission), #POST, {'mentor': , 'member': , 'task_name': , 'task_num': , 'track': }
    path('member/pending_review/', views.pending_review), #POST, {'mentor': that is, the current user}
    path('member/display_submission/', views.display_submission), #POST, {'mentor': still the current user itself}
    path('member/mentor_eval/', views.mentor_eval), #POST, {'mentor': , 'feedback': , 'accepted': boolean, 'task_name': , 'task_num': }
    path('member/task_leaderboard/', views.task_leaderboard), #POST, {'task_name': , 'task_num': , 'track': }
    path('member/track_leaderboard/', views.track_leaderboard) #POST, {'track': }
]