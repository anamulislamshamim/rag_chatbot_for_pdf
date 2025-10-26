from rest_framework import serializers


class ChatRequestSerializers(serializers.Serializer):
    question = serializers.CharField(required=True)

