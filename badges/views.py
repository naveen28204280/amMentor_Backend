from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import json
from .models import Badges
from .models import Badges_Members
from members.models import Members

User = get_user_model()
# Create your views here.
def make_badge(request):
    if not request.user.is_superuser:
        return JsonResponse({"error": "Only superusers can delete badges"}, status=403)
    try:
        data=json.loads(request.body)
        if not all(b in data for b in ['badge', 'icon']):
            return JsonResponse({'error: ': 'Missing required fields'}, status=400)
        Badges.objects.create(
            badge=data['badge'],
            icon=data['icon']
        ) 
        return JsonResponse({'Successfully created':  data["badge"]}, status=200)
    except Exception as e:
        return JsonResponse({"error found: ": e}, status=500)
    
def delete_badge(request):
    try:
        data=json.loads(request.body)
        if not data['badge']:
            return JsonResponse({'error': 'Missing required fields'})
        Badges.objects.filter(badge=data['badge']).delete()
        return JsonResponse({"Succesfully deleted: ": data['badge']}, status=200)
    except Exception as e:
        return JsonResponse({"error found: ": e}, status=500)
    
def assign_badge(request):
    try:
        data=json.loads(request.body)
        if not all(d in data for d in ['badge', 'member']):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        badge=Badges.objects.get(badge=data['badge'])
        member=Members.objects.get(name=data['member'])
        if not badge:
            return JsonResponse({'error': 'Badge not found'}, status=400)
        if not member:
            return JsonResponse({'error': 'Member not found'}, status=400)
        prev=Badges_Members.objects.get(badge=badge, member=member)
        if not prev:
            Badges_Members.objects.create(
                badge=badge,
                member=member
            )
            return JsonResponse({'Succesfully assigned badge': data['badge']}, status=200)
        else:
            return JsonResponse({'error': f"{data['member']} already has this badge"})
    except Exception as e:
        return JsonResponse({"error found: ": e}, status=500)
    
def badges_earned(request):
    try:
        data=json.loads(request.body)
        if not data['member']:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        member=Members.objects.get(name=data['member'])
        badges=Badges_Members.objects.filter(member=member).values_list('badge__badge', flat=True)
        return JsonResponse({"badges earned": list(badges)}, status=200)
    except Exception as e:
        return JsonResponse({"error": e}, status=500)