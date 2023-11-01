from django.contrib.auth import authenticate
from rest_framework import serializers


class MagicLinkSerializer(serializers.Serializer):
    email = serializers.CharField(label="email", write_only=True, required=True)
    name = serializers.CharField(required=False)
    group_id = serializers.IntegerField(required=False)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(label="email", write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        request = self.context.get("request")
        token = attrs.get("token")

        if email and token:
            user = authenticate(request=request, email=email, token=token)
            if not user:
                error_message = "Access denied: Invalid email or token"
                raise serializers.ValidationError(error_message, code="authorization")
        else:
            error_message = 'Both "email" and "token" are required.'
            raise serializers.ValidationError(error_message, code="authorization")

        attrs["user"] = user
        return attrs
