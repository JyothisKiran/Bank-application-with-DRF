from rest_framework import serializers
from .models import BankDetailModel,User


class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetailModel
        fields = '__all__'

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','email','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    """func. b/w view and models"""
    
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
