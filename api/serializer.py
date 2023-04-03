from users.models import User, UserAvatar, UserLocation
from rest_framework import serializers, validators
from django.contrib.auth.password_validation import validate_password

#user serializer
class UserAvatarSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    avatar = serializers.FileField()
    class Meta:
        model = UserAvatar
        fields = ("id","user", "avatar")   


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_type')


class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")
        extra_kwarg = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            "email": {
            "required": True,
            "allow_blank": False,
            "validators": [
            validators.UniqueValidator(
                User.objects.all(), "Account with that Email already exists"
            )
            ]
            },
         }
        
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email
        )

        user.set_password(validated_data['password1'])
        user.save()

        return user
    


 


