from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import CustomUser, Subscribe


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')
        read_only_fields = 'id', 'is_subscribed'

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(
            subscribed=self.context['request'].user,
            user=obj.id).exists()
