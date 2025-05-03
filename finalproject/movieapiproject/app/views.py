from django.shortcuts import render
from .models import Movie
from .serializer import MovieSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
class Allmovie(generics.ListAPIView):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer

@api_view(['GET'])
def apioverview(req):
    api_url={
        'allmovies':"/Allmovie",
        'addmovies':"/Addmovie",
        "updatemovie":'/Updatemovie/update/pk',
        "deletemovie":'/Deletemovie/delete/pk',
        'search by category':'/searchbycategory/?category=categoryname'
    }
    return Response(api_url)

class Addmovie(generics.ListCreateAPIView):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer

class Updatemovie(generics.RetrieveUpdateAPIView):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer

class Deletemovie(generics.DestroyAPIView):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer

from django.db.models import Q
from rest_framework import status

@api_view(['GET'])
def searchbycategory(req):
    query_params=req.query_params
    filters=Q()

    if "category" in query_params:
        filters &=Q(category=query_params['category'])

    movies=Movie.objects.filter(filters)
    if not movies.exists():
        return Response(
            {'message':'No movie found'},status=status.HTTP_404_NOT_FOUND
        )
    serializer=MovieSerializer(movies,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)