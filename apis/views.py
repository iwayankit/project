# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from apis.serializers import ArticleSerializer
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Article
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging


# Create your views here.

logging = logging.getLogger(__name__)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    logging.info("login_called_with_paylaod = {}".format(request.data))
    username = request.data['username']
    password = request.data['password']
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=status.HTTP_200_OK)


@api_view(["GET"])
def get_user(request):
    logging.info("get_user_called_with_user_name = {}".format(request.GET.get("userName")))
    userName = request.GET.get("userName")
    if userName is None:
        return Response({'error': 'Please provide user name'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=userName)
        result = {
            "name": user.username,
            "email": user.email
        }
    except Exception as e:
        return Response({"error = {}".format(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'result': result}, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_article(request):
    logging.info("create_article_called_with_paylaod = {}".format(request.data))
    serializer = ArticleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    try:
        Article.objects.create(**data)
    except Exception as e:
        return Response({"error = {}".format(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
def update_article(request):
    logging.info("update_article_called_with_paylaod = {}".format(request.data))
    serializer = ArticleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    try:
        Article.objects.filter(id=request.data['articleId']).update(**data)
    except Exception as e:
        return Response({"error = {}".format(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_article(request):
    article_id = request.GET.get("articleId")
    if article_id is None:
        return Response({'error': 'Please provide article id'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        article = Article.objects.get(id=article_id)
        result = {
            "headline": article.headline,
            "content": article.content
        }
    except Exception as e:
        return Response({"error = {}".format(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(result, status=status.HTTP_200_OK)

