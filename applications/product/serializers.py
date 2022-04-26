from rest_framework import serializers

from applications.product.models import Element, Category, ElementImage


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementImage
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ElementSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    image = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Element
        fields = ('title', 'user', 'price', 'category', 'description', 'image')

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        element = Element.objects.create(**validated_data)
        for image in images_data.getlist('images'):
            ElementImage.objects.create(element=element, image=image)
        return element

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['like'] = instance.like.filter(like=True).count()
        return representation


