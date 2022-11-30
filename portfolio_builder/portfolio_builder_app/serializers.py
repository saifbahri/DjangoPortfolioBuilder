from rest_framework import serializers
from .models import *


        
       


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'name', 'phone', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
            password = validated_data.pop('password', None)
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance


class BiographySerializer(serializers.ModelSerializer):
    class Meta:
        model=Biography
        fields='__all__' 



        

class professional_accomplishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=professional_accomplishment
        fields='__all__'




class social_mediaSerializer(serializers.ModelSerializer):
    class Meta:
        model=social_media
        fields='__all__' #serializes all fields
        #fields=('id','name','familyName','group') #serializes only these fields



class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model=Portfolio
        fields='__all__' 



class professional_accomplishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=professional_accomplishment
        fields='__all__'  



class awardSerializer(serializers.ModelSerializer):
    class Meta:
        model=award
        fields='__all__'

        

class justificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=justification
        fields='__all__'
           

class certificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=certification 
        fields='__all__' 


class community_serviceSerializer(serializers.ModelSerializer):
    class Meta:
        model=community_service
        fields='__all__'


class   referenceSerializer(serializers.ModelSerializer):
    class Meta:
        model=  reference
        fields='__all__'




