from djoser.serializers import UserSerializer
from .models import CustomUser, Subscribe
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
        read_only_fields = 'id', 'is_subscribed'

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(subscribed=self.context['request'].user,
                                        user=obj.id).exists()

class SubscribeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    #user = serializers.SlugRelatedField(
    #    read_only=True, slug_field='username')
    class Meta:
        model = Subscribe
        fields = 'user'
        #fields = ('subscribe.user.email', 'subscribe_user__id', 'subscribe_user__name', 'user_is_subscribed')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=('subscribed', 'user'))]

    def validate(self, data):
        if self.context['request'].user == data['user']:
            raise serializers.ValidationError(
                'На себя нельзя подписываться!')
        return data
