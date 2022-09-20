from rest_framework import serializers
# from projects.models import Project, Tag, Review

from users.models import Profile, Heart

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class HeartSerializers(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)

    class Meta:
        model = Heart
        fields = '__all__'