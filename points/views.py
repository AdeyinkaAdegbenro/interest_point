from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from .models import InterestPoint, SharedInterest
from points.serializers import InterestPointSerializer , UserSerializer, SharedInterestSerializer

# Create your views here.

def home(request):
    ''' 
        this view fetches the home page of the application
    '''
    return render(request, 'entry.html', context={})

@csrf_exempt
def index(request):
    ''' 
        this view creates a new interest point and
        also fetches existing interest points
    '''

    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        if request.method == 'GET':
            pts = InterestPoint.objects.filter(user=user).all()
            serializer = InterestPointSerializer(pts, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif request.method == 'POST':
            
            data = JSONParser().parse(request)
            serializer = InterestPointSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=user)
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            interest = InterestPoint.objects.filter(user=user, pk=data['id']).first()
            print('interest', interest.name, interest.latitude, interest.user)
            serializer = InterestPointSerializer(interest, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({"message": "Not authorized"}, status=400)

def users(request):
    ''' 
        this view fetches other users excluding 
        the logged in user
    '''
    if request.user.is_authenticated:
        if request.method == 'GET':
            users = User.objects.filter().exclude(id=request.user.id).all()
            serializer = UserSerializer(users, many=True)
            return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({"message": "Not authorized"}, status=403)

def share(request):
    ''' 
        this view is used to share an interest point with other users.
        It also fetches interest points shared with logged in user.
    '''
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        if request.method == 'GET':
            shared_with_me = SharedInterest.objects.filter(shared_user=user).all()
            serializer = SharedInterestSerializer(shared_with_me, many=True)
            return JsonResponse(serializer.data, safe=False)
        if request.method == 'POST':
            data = JSONParser().parse(request)
            shared_user = User.objects.get(pk=data['shared_user'])
            interest = InterestPoint.objects.get(pk=data['interest_id'])
            serializer = SharedInterestSerializer(data=data)
            if serializer.is_valid():
                serializer.save(shared_user=shared_user, interest=interest)
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({"message": "Not authorized"}, status=403)