from rest_framework import serializers


class MagicLinkSerializer(serializers.Serializer):
    email = serializers.CharField(label="email", write_only=True, required=True)
    name = serializers.CharField(required=False)
    group_id = serializers.IntegerField(required=False)
