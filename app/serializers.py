from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import *



# class ProductSerializer(ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'



class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        # fields = ['id', 'name', 'country']

class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class BookSerializer(ModelSerializer):
    # author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    # genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)
    # currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())

    class Meta:
        model = Book
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['id']
    #     representation['author'] = AuthorSerializer(instance.author).data
    #     representation['genres'] = GenreSerializer(instance.genres.all(), many=True).data
    #     representation['currency'] = CurrencySerializer(instance.currency).data
    #     return representation

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined']

class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email'
        ]
class PurchaseItemSerializer(ModelSerializer):

    class Meta:
        model = PurchaseItem
        fields = [
            'book', 'quantity', 'subtotal'
        ]



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(representation)
        representation['book'] = BookSerializer(instance.book, many=False).data
        # print(representation)
        # representation['book'].pop('id')
        representation['book'].pop('author')
        representation['book'].pop('publication_year')
        representation['book'].pop('genres')
        representation['book'].pop('image')
        representation['book'].pop('description')
        representation['book'].pop('audio')
        representation['book'].pop('video')
        representation['book'].pop('currency')
        representation['book']['price']
        return representation
class PurchaseSerializer(ModelSerializer):
    items = PurchaseItemSerializer(many=True, read_only=True)  # Используем PurchaseItemSerializer для сериализации
    class Meta:
        model = Purchase
        fields = [
            'items', 'total', 'created_at'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = instance.created_at.strftime("%d-%m-%Y %H:%M:%S")
        representation['items'] = PurchaseItemSerializer(instance.items.all(), many=True).data
        return representation
        # representation['items'] = []
        # for elem in instance.items.all():
        #     representation['items'].append({
        #         'book': elem.book.name,
        #         'quantity': elem.quantity,
        #         'subtotal': elem.subtotal
        #     })
        #
        # return representation


    # temp = representation['create_at'].split('T')
    # date = temp[0]
    # time = temp[1].split('.')[0]
    # representation['create_at'] = f"{date} {time}"

# 1) Перегрузить метод to_representation так, чтобы поле product показывал все поля
# Для этого, нужно использовать ProductSerializer

# class UserTestSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'