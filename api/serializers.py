from rest_framework import serializers

from api.models import Work


class WorkSerializer(serializers.ModelSerializer):
    contributors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Work
        fields = ['title', 'contributors']


class WorkEnrichSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    iswc = serializers.ListField(child=serializers.CharField())
