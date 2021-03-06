from rest_framework import serializers

from applications.product.models import Element
from applications.review.models import Like, Rating, Comment


class RatingSerializer(serializers.ModelSerializer):
    """
    Сериализатор рейтинга
    """
    class Meta:
        model = Rating
        fields = ('rating', )


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор отзывов
    """
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Comment
        fields = '__all__'


class RetriveReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального отзыва
    """
    class Meta:
        model = Element
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['review'] = ReviewSerializer(instance.comment.all(), many=True).data
        return representation

# TODO dqw