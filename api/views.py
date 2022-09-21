from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Heart

from .serializers import HeartSerializers


@api_view(["GET"])
def getRoutes(request):

    routes = [
        {"GET": "/api/hearts"},
        {"POST": "/api/users/token"},
        {"POST": "/api/users/token/refresh"},
    ]
    return Response(routes)


@api_view(["GET"])
def getHeart(request):
    user = request.user.profile
    print(user)
    heart = Heart.objects.get(owner=user)
    serializer = HeartSerializers(heart, many=False)
    return Response(serializer.data)


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
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     user = request.user.profile
    #     heart = Heart.objects.get(owner=user)
    #     heart.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
