from rest_framework import serializers
from users.models import Heart, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class HeartSerializers(serializers.ModelSerializer):
    # owner = ProfileSerializer(many=False)

    class Meta:
        model = Heart
        # fields = "__all__"
        exclude = ("id", "owner")
