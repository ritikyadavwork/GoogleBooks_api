import requests
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.shortcuts import render
from .api import fetch_books_api
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .models import Recommendation, UserInteraction
from .serializers import RecommendationSerializer, UserInteractionSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


def search_books(request):
    context = {}
    author = request.GET.get('author')
    category = request.GET.get('category')
    keyword = request.GET.get('keyword')

    if author or category or keyword:
        books = fetch_books_api(keyword, author, category)
        context['books'] = books

        if 'error' in books:
            return JsonResponse(books, status=400)

    return render(request, 'search.html', context)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_recommendation(request):
    serializer = RecommendationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_recommendations(request):
    recommendations = Recommendation.objects.all()
    serializer = RecommendationSerializer(recommendations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def filter_recommendations(request):
    genre = request.GET.get('genre')
    rating = request.GET.get('rating')
    date = request.GET.get('date')

    recommendations = Recommendation.objects.all()

    if genre:
        recommendations = recommendations.filter(genre__iexact=genre)
    if rating:
        recommendations = recommendations.filter(rating__gte=rating)
    if date:
        recommendations = recommendations.filter(publication_date__gte=date)

    serializer = RecommendationSerializer(recommendations, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_interaction(request):
    serializer = UserInteractionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
