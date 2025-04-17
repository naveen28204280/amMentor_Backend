from django.shortcuts import render
from django.contrib.auth import get_user_model
import json
from .models import Tracks, Curriculum, Submissions, Tasks
from django.http import JsonResponse
from members.models import Members
from django.utils.timezone import now, timedelta

User=get_user_model()

# Create your views here.
def create_track(request):
    if not request.user.is_superuser:
        return JsonResponse({"error": "Only superusers can delete tracks"}, status=403)
    try:
        data=json.loads(request.body)
        if not data['track']:
            return JsonResponse({'error': e})
        Tracks.objects.create(
            track=data['track'],
        )
        return JsonResponse({"Successfully created": f"{data['track']}"}, status=200)
    except Exception as e:
        return JsonResponse({"error": f'{e}'}, status=500)
    
def delete_track(request):
    if not request.user.is_superuser:
        return JsonResponse({"error": "Only superusers can delete tracks"}, status=403)
    try:
        data=json.loads(request.body)
        del_track = Tracks.objects.get(track=data['track'])
        related_tasks = Tasks.objects.filter(track=del_track)
        Submissions.objects.filter(task__in=related_tasks).delete()
        related_tasks.delete()
        del_track.delete()
        return JsonResponse({'Successfully deleted': data['track']}, status=200)
    except Exception as e:
        return JsonResponse({"error": e}, status=500)
    
def create_task(request):
    if not request.user.is_superuser:
        return JsonResponse({"error": "Only superusers can remove members"}, status=403)
    try:
        data=json.loads(request.body)
        try:
            track=Tracks.objects.get(track=data['track'])
        except Tracks.DoesNotExist:
                return JsonResponse({"error": "Track not found"}, status=404)
        if not all(t in data for t in ['task_name', 'task_num', 'task_description', 'points', 'deadline', 'track']):
            return JsonResponse({"error": "Missing required fields"}, status=400)
        Tasks.objects.create(
            task_name=data['task_name'],
            task_num=data['task_num'],
            task_description=data['task_description'],
            points=data['points'],
            deadline=data['deadline'],
            track=track
        )
        return JsonResponse({"Succesfully created task: ": data['task_name']}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"{e}"}, status=403)
    
def delete_task(request):
    if not request.user.is_superuser:
        return JsonResponse({"error": "Only superusers can delete tracks"}, status=403)
    try:
        data=json.loads(request.body)
        if not all(d in data for d in ['task_num', 'task_name', 'track']):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        track=Tracks.objects.get(track=data['track'])
        task=Tasks.objects.get(task_num=data['task_num'], task_name=data['task_name'], track=track)
        task_name = task.task_name
        Tasks.objects.filter(task_num=data['task_num'], task_name=data['task_name'], track=track).delete()
        task.delete()
        return JsonResponse({"Succesfully deleted": task_name})
    except Exception as e:
        return JsonResponse({"error": e}, status=500)
    
def display_tracks(request):
    try:
        tracks=Tracks.objects.all().values_list('track', flat=True)
        return JsonResponse({"tracks": list(tracks)}, status=200)
    except Exception as e:
        return JsonResponse({"error": e}, status=500)
    
def select_track(request):
    try:
        data=json.loads(request.body)
        if not all(i in data for i in ['track', 'member']):
            return JsonResponse({"error": "Missing required fields"}, status=400)
        member=Members.objects.get(name=data['member'])
        track=Tracks.objects.get(track=data['track'])
        member.track= track
        member.save()
        return JsonResponse({"Succesfully changed track": data['track']}, status=200)
    except Tracks.DoesNotExist:
        return JsonResponse({"error": "Track not found"}, status=404)
    except Members.DoesNotExist:
        return JsonResponse({"error": "Member not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": e}, status=500)

def display_all_tasks(request):
    try:
        data = json.loads(request.body)
        if not data.get('member'):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        member = Members.objects.get(name=data['member'])
        track=member.track
        tasks = Tasks.objects.filter(track=track)
        tasks_data = []
        for task in tasks:
            curriculum_row = Curriculum.objects.filter(task=task, member=member).first()
            if curriculum_row:
                if curriculum_row.end:
                    status = 'finished'
                elif curriculum_row.start:
                    status = 'ongoing'
                else:
                    status = 'upcoming'
            tasks_data.append({
                'task_name': task.task_name,
                'task_num': task.task_num,
                'points': task.points,
                'deadline': task.deadline,
                'status': status if curriculum_row else "upcoming",
                'track': member.track.track
            })
        return JsonResponse({"tasks": tasks_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    except Tracks.DoesNotExist:
        return JsonResponse({'error': 'No such track found'}, status=404)

def display_task_details(request):
    try:
        data=json.loads(request.body)
        if not all(d in data for d in ['task_name', 'task_num', 'member']):
            return JsonResponse({'error': 'Missing required fields'})
        member=Members.objects.get(name=data['member'])
        track=member.track
        task = Tasks.objects.get(task_name=data['task_name'], track=track, task_num=data['task_num'])
        curriculum_row=Curriculum.objects.get(task=task)
        submissions=Submissions.objects.filter(task=task, member=member)
        if submissions:
            paused_time=timedelta()
            for s in submissions:
                paused_time+=s.pause_end-s.pause_start
            if curriculum_row.end:
                days_worked=curriculum_row.end-curriculum_row.start-paused_time 
            else:
                days_worked=now()-curriculum_row.start-paused_time
            days_left=timedelta(days=task.deadline)-days_worked
        task_data= {
            "task_name": task.task_name,
            "task_num": task.task_num,
            "task_description": task.task_description,
            "deadline": task.deadline,
            "points": task.points,
            "track": task.track.track,
            "start_date": curriculum_row.start if curriculum_row.start else None,
            "end_date": curriculum_row.end if curriculum_row.end else None,
            "days_left": days_left if curriculum_row.start and not curriculum_row.end else None,
            "days_worked": days_worked.days if curriculum_row.start else None
        }
        return JsonResponse(task_data, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)})

def start_task(request):
    try:
        data=json.loads(request.body)
        if not all(t in data for t in ['task_name', 'task_num', 'member']):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        member = Members.objects.get(name=data['member'])
        track=member.track
        task=Tasks.objects.get(task_name=data['task_name'], task_num=data['task_num'], track=track)
        if not task:
            return JsonResponse({'error': 'Task not found'}, status=404)
        Curriculum.objects.create(
            member=member,
            task=task,
        )
        return JsonResponse({"Started Task: ": data['task_name']}, status=200)
    except Tracks.DoesNotExist:
        return JsonResponse({"error": "Track not found"}, status=404)
    except Members.DoesNotExist:
        return JsonResponse({"error": "Member not found"}, status=404)
    except Tasks.DoesNotExist:
        return JsonResponse({"error": "Tasks not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f'{e}'}, status=500)
    
def pause_task(request):
    try:
        data=json.loads(request.body)
        if not all(t in data for t in ['mentor', 'task_name', 'task_num']):
            return JsonResponse({'error': 'Missing required fields'})
        mentor=Members.objects.get(name=data['mentor'])
        member=mentor.mentee
        track=mentor.mentee.track
        task=Tasks.objects.get(task_name=data['task_name'], task_num=data['task_num'], track=track)
        Submissions.objects.create(
            member=member,
            task=task
        )
        return JsonResponse({'paused': task.task_name})
    except Exception as e:
        return JsonResponse({'error': e}, status=500)
    except Members.DoesNotExist:
        return JsonResponse({'error': 'Mentor or Mentee not found'}, status=404)
    except Tasks.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

def resume_task(request):
    try:
        data=json.loads(request.body)
        if not all(t in data for t in ['mentor', 'member', 'task_name', 'task_num']):
            return JsonResponse({'error': 'Missing required fields'})
        mentor=Members.objects.get(name=data['mentor'])
        member=mentor.mentee
        track=member.track
        task=Tasks.objects.get(task_name=data['task_name'], task_num=data['task_num'], track=track)
        submission=Submissions.objects.get(member=member, task=task)
        submission.pause_end=now()
        submission.save()
        return JsonResponse({'resumed': task.task_name}, status=200)
    except Exception as e:
        return JsonResponse({'error': e}, status=500)
    except Submissions.DoesNotExist:
        return JsonResponse({'error': 'No paused submission found for this task'}, status=404)
    except Members.DoesNotExist:
        return JsonResponse({'error': 'Mentor or Mentee not found'}, status=404)
    except Tasks.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    
def mentee_submission(request):
    try:
        data=json.loads(request.body)
        if not all(s in data for s in ['mentor', 'member', 'task_name', 'task_num', 'sub_url']):
            return JsonResponse({"error": "Missing required fields"}, status=400)
        member= Members.objects.get(name=data['member'], mentor=data['mentor'])
        track=member.track
        task = Tasks.objects.get(task_name=data['task_name'], task_num=data['task_num'], track=track)
        Submissions.objects.create(
            member=member,
            task=task,
            mentor=member.mentor
        )
        return JsonResponse({"Succesfully submitted": data['task_name']}, status=200)
    except Exception as e:
        return JsonResponse({"error": e}, status=500)

def pending_review(request):
    try:
        data=json.loads(request.body)
        if not data['mentor']:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        mentor=Members.objects.get(name=data['mentor'])
        mentee=mentor.mentee
        submission=Submissions.objects.get(
            member=mentee, 
            pause_end=None,
            feedback=None,
            accepted=None,
            sub_url__isnull= False
            )
        if submission:
            return JsonResponse({
                True: 'Pending review'
            }, status=200)
        else:
            return JsonResponse({False: 'No pending reviews'}, status=200)
    except Exception as e:
        return JsonResponse({'error': e}, status=500)

def display_submission(request):
    try:
        data=json.loads(request.body)
        if not data['mentor']:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        mentor=Members.objects.get(name=data['mentor'])
        mentee=mentor.mentee
        submission=Submissions.objects.get(
            member=mentee, 
            pause_end=None,
            feedback=None,
            accepted=None,
            sub_url__isnull= False
            )
        if submission:
            return JsonResponse({
                "task_name": submission.task.task_name,
                "task_num": submission.task.task_num,
                "sub_url": submission.sub_url,
                "mentee": submission.member.name,
                "submitted_on": submission.pause_start
            }, status=200)
        else:
            return JsonResponse({'message': 'No pending reviews'}, status=200)
    except Exception as e:
        return JsonResponse({'error': e}, status=500)

def mentor_eval(request):
    try:
        data=json.loads(request.body)
        if not all(t in data for t in ['mentor', 'feedback', 'accepted', 'task_name', 'task_num']):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        task=Tasks.objects.get(task_name=data['task_name'], task_num=data['task_num'])
        mentor=Members.objects.get(name=data['mentor'])
        mentee=mentor.mentee
        submission=Submissions.objects.get(member=mentee, task=task, pause_end__isnull=True, feedback__isnull=True, accepted__isnull=True)
        submission.feedback=data['feedback']
        submission.accepted=data['accepted']
        submission.pause_end=now()
        submission.save()
        if data['accepted']==True:
            curriculum=Curriculum.objects.get(member=mentee, task=task)
            curriculum.end=now()
            curriculum.save()
            if (curriculum.start-curriculum.end + submission.pause_start - submission.pause_end)<= task.deadline:
                mentee.points+= task.points
            else:
                mentee.points += task.points//2
                return JsonResponse({True: 'Completed task'}, status=200)
        else:
            return JsonResponse({False: 'Continue task'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def task_leaderboard(request):
    try:
        data=json.loads(request.body)
        if not all(k in data for k in ['task_name', 'task_num', 'track']):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        track=Tracks.objects.get(track=data['track'])
        task=Tasks.objects.get(task_name=data['task_name'], task_num=data['task_num'], track=track)
        curriculum_entries=Curriculum.objects.filter(task=task, end__isnull=False)
        leaderboard=[]
        for entry in curriculum_entries:
            submissions =Submissions.objects.filter(member=entry.member, task=task, accepted=True)
            if not submissions.exists():
                continue
            total_pause=timedelta()
            for sub in Submissions.objects.filter(member=entry.member, task=task):
                if sub.pause_start and sub.pause_end:
                    total_pause += (sub.pause_end - sub.pause_start)
            time_spent=(entry.end - entry.start) - total_pause
            leaderboard.append({
                'name': entry.member.name,
                'days_spent': time_spent.days
            })
        leaderboard.sort(key=lambda x: x['days_spent'])
        return JsonResponse(leaderboard, safe=False, status=200)
    except Tasks.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def track_leaderboard(request):
    try:
        data=json.loads(request.body)
        if not data['track']:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        track=Tracks.objects.get(track=data['track'])
        tasks=Tasks.objects.filter(track=track)
        curriculum_rows=Curriculum.objects.filter(task__in=tasks, end__isnull=False)
        leaderboard={}
        for row in curriculum_rows:
            member=row.member
            task=row.task
            submissions=Submissions.objects.filter(member=member, task=task, pause_end__isnull=False)
            paused_time=timedelta()
            for s in submissions:
                paused_time+=s.pause_end - s.pause_start
            days_worked=(row.end - row.start - paused_time).days
            if member.name not in leaderboard:
                    leaderboard[member.name] = {
                        "tasks_completed": 0,
                        "total_days": 0
                    }
            leaderboard[member.name]['tasks_completed']+=1
            leaderboard[member.name]['total_days']+=days_worked
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: (-x[1]['tasks_completed'], x[1]['total_days']))
        leaderboard = [{name: stats} for name, stats in sorted_leaderboard]
        return JsonResponse(leaderboard, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)