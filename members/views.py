from django.http import HttpResponse, JsonResponse
from members.models import Members
from django.contrib.auth import get_user_model
import json
from curriculum.models import Tracks
from django.core.mail import send_mail
import random
from django.contrib.auth import logout, login

User = get_user_model()

def create_member(request):
    if not request.user.is_superuser:
        return JsonResponse({"error": "Only superusers can remove members"}, status=403)
    try:
        data=json.loads(request.body)
        if not data or not all(field in data for field in ['name', 'discord', 'github', 'email', 'group']):
            return JsonResponse({'error: ': 'Missing required fields'}, status=400)
        name=data['name']
        discord=data['discord']
        github=data['github']
        email=data['email']
        group=data['group']
        if Members.objects.filter(github=github).exists() or Members.objects.filter(discord=discord).exists():
            return JsonResponse({"A user already exists with the name": data['name']}, status=409)
        else:
            Members.objects.create(
                name=name,
                discord=discord,
                github=github,
                email=email,
                group=group
            )
            return JsonResponse({"Added member: ": name}, status=200)
    except Exception as e:
        return JsonResponse({"error": e}, status=500)
    
def delete_member(request):
    if not request.user.is_superuser:
        return JsonResponse({"error": "Only superusers can remove members"}, status=403)
    try:
        data=json.loads(request.body)
        member=data['member']
        if not Members.objects.filter(name=member['name']):
            return JsonResponse({'error: ': 'Member not found'}, status=400)
        else:
            Members.objects.filter(name=member['name']).delete()
            return HttpResponse(f"{member['username']} has been removed")
    except Exception as e:
        return JsonResponse({"error": e}, status=500)

def mail_member(request):
    try:
        data=json.loads(request.body)
        if not data['email']:
            return JsonResponse({"error": "Missing required fields"}, status=400)
        otp=random.randint(100000,999999)
        request.session['otp'] = str(otp)
        request.session['email'] = data['email']
        send_mail(
            subject="OTP for amMentor login",
            message=f"{otp} is your OTP for logging in to amMentor",
            from_email="our_email@gmail.com", #amFOSS mail
            recipient_list=[data['email']],
            fail_silently=False,
        )
        return JsonResponse({"Successfully sent OTP": "Sent OTP"}, status=200)
    except Exception as e:
        return JsonResponse({"error": e}, status=500)
    
def verify_otp(request):
    try:
        data = json.loads(request.body)
        if not data.get('otp'):
            return JsonResponse({"error": "Missing OTP"}, status=400)
        session_otp = request.session.get('otp')
        email=request.session.get('email')
        if session_otp and data['otp'] == session_otp:
            user = Members.objects.get(email=email)
            if user:
                login(request,User)
                return JsonResponse({"verified": True}, status=200)
            else:
                return JsonResponse({"verified": False}, status=401)
    except Exception as e:
        return JsonResponse({"error": e}, status=500)
    
def member_details(request):
    try:
        data=json.loads(request.body)
        if not any(t in data for t in ['email', 'name']):
            return JsonResponse({"error": "Missing required fields"}, status=400)
        if data.get('email'):
            member=Members.objects.get(email=data['email'])
        if data.get('name'):
            member=Members.objects.get(name=data['name'])
        member_data = {
            'name': member.name,
            'email': member.email,
            'discord': member.discord,
            'github': member.github,
            'mentor': member.mentor.name if member.mentor else None,
            'mentee': member.mentee.name if member.mentor else None,
            'year': member.year,
            'points': member.points if member.points else None,
            'group': member.group,
            'track': member.track.track if member.track else None,
            'pfp': member.pfp.url,
        }
        return JsonResponse(member_data, status=200)
    except Exception as e:
        return JsonResponse({"error": e}, status=500)
    
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"message": "Successfully logged out"}, status=200)
    else:
        return JsonResponse({"error": "User is not logged in"}, status=400)

def assign_mentor(request):
    try:
        data=json.loads(request.body)
        if not all(i in data for i in ['mentor', 'mentee']):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        mentor=Members.objects.get(name=data['mentor'])
        mentee=Members.objects.get(name=data['mentee'])
        mentee.mentor=mentor
        mentor.mentee=mentee
        mentor.save()
        mentee.save()
        return JsonResponse({'Successfully assigned': data['mentor']}, status=200)
    except Exception as e:
        return JsonResponse({'error': e})

def select_track(request):
    try:
        data=json.loads(request.body)
        if not all(d in data for d in ['name', 'track_name']):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        track=Tracks.objects.get(name=data['track'])
        member=Members.objects.get(name=data['name'])
        member.track=Tracks.objects.get(track=track)
        member.save()
        return JsonResponse({'success': 'Updated track'}, status=200)
    except Exception as e:
        return JsonResponse({'error': e}, status=500)
    
def customize(request):
    try:
        data=json.loads(request.body)
        if not data['name']:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        member=Members.objects.get(name=data['name'])
        updatable_fields = ['discord', 'github', 'email', 'pfp', 'group', 'year', 'track']
        for field in updatable_fields:
            if field in data:
                setattr(member, field, data[field])
        member.save()
        return JsonResponse({'message': 'Profile updated'}, status=200)
    except Exception as e:
        return JsonResponse({'error': e}, status=500)
    
def leaderboard_points(request):
    try:
        members = Members.objects.all().order_by('-points')
        data = [{'name': member.name, 'points': member.points} for member in members]
        return JsonResponse(data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': e}, status=500)