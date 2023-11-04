from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)  # Parolni write_only=True sifatida qo'shing

    class Meta:
        model = User
        fields = ('id', 'is_superuser', 'username', 'password')



class MahsulotTuriSerializer(ModelSerializer):
    class Meta:
        model = Mahsulot_turi
        fields = '__all__'


class ChiqimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chiqim
        fields = '__all__'


class MahsulotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahsulot
        fields = '__all__'

    def create(self, validated_data):
        chiqim_data = {
            'summa': validated_data['narx1'] * validated_data['miqdor'],
            'izoh': f"{validated_data['nom']} {validated_data['miqdor']}",
            'masul': None,
            'sana': validated_data['sana']
        }
        chiqim = Chiqim.objects.create(**chiqim_data)

        mahsulot_data = {
            "nom": validated_data['nom'],
            "turi": validated_data['turi'],
            "narx1": validated_data['narx1'],
            "narx2": validated_data['narx2'],
            "miqdor": validated_data['miqdor'],
            "izoh": validated_data['izoh'],
            "sana": validated_data['sana']
        }
        mahsulot = Mahsulot.objects.create(**mahsulot_data)

        return mahsulot


class MijozSerializer(ModelSerializer):
    class Meta:
        model = Mijoz
        fields = '__all__'


class SavdoSerializer(ModelSerializer):
    class Meta:
        model = Savdo
        fields = '__all__'

    # def create(self, validated_data):
    #     summa = validated_data['summa']
    #     mijoz = Mijoz.objects.get(id=validated_data['mijoz'])
    #     mijoz.summa = summa + mijoz.summa
    #     mijoz.save()
    #
    #     return mijoz


class ChiqimSerializer(ModelSerializer):
    class Meta:
        model = Chiqim
        fields = '__all__'


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         # Add custom claims to the token payload
#         token['id'] = user.id
#         token['username'] = user.username
#         token['password'] = user.password
#         return token