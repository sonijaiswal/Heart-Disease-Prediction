from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Heart

from .serializers import HeartSerializers

# ================================================================================
from datetime import datetime

from rest_framework import serializers

from rest_framework.renderers import JSONRenderer


class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()


class CommentSerializers(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()


comment = Comment(email="leila@email.com", content="foo bar")

serializer = CommentSerializers(comment)

json = JSONRenderer().render(serializer.data)
print(json)

# =================================================================================


@api_view(["GET"])
def getRoutes(request):

    routes = [
        {"GET": "/api/heart"},
        {"POST": "/api/users/token"},
        {"POST": "/api/users/token/refresh"},
    ]
    return Response(routes)


class HeartDetail(APIView):
    def get_object(self, request):
        try:
            user = request.user.profile
            return Heart.objects.get(owner=user.username)
        except Heart.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        user = request.user.profile
        heart = Heart.objects.get(owner=user)
        serializer = HeartSerializers(heart)
        return Response(serializer.data)

    def put(self, request, format=None):
        user = request.user.profile
        heart = Heart.objects.get(owner=user)
        serializer = HeartSerializers(heart, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET"])
# def getHeart(request):
#     user = request.user.profile
#     print(user)
#     heart = Heart.objects.get(owner=user)
#     serializer = HeartSerializers(heart, many=False)
#     return Response(serializer.data)
