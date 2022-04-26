from rest_framework import serializers

from applications.review.models import Like, Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('rating', )

