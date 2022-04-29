from rest_framework import serializers

from applications.product.models import Element, Category, ElementImage, FavouriteElement, Reservation, HotelsIk



import requests

from applications.product.sendmessage import sendTelegram
from applications.telebot.models import TeleSettings

token = '5350539323:AAEDs7_ttU8d84egZTdqsG977AKbXRd36GA'
chat_id = '-566077291'
text = 'admindnq'







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
        representation['reviews'] = instance.comment.count()

        rating_result = 0
        for i in instance.rating.all():
            rating_result += int(i.rating)

        if instance.rating.all().count() == 0:
            representation['rating'] = rating_result

        else:
            representation['rating'] = rating_result / instance.rating.all().count

        return representation


class FavouriteElementSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = FavouriteElement
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Reservation
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print('-----------------------')
        print(instance)
        representation['element'] = ElementSerializer(instance.element).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        print(request.data.get('element'))
        a = request.data.get('element')
        # TODO find
        b = Element.objects.get(a)
        print(b)

        sendTelegram(request.data.get('phone'), request.data.get('element'))
        print(request.data.get('phone'))
        create = super().create(validated_data)
        return create

