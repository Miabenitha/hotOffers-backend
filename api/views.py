from rest_framework.decorators import api_view, permission_classes
from users.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.utils import send_verification_email
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from api.serializer import(
    UserSerializer,
    RegisterUserSerializer,
    UserAvatarSerializer 
    )


@api_view(['POST'])
def signup(request):
    serializer = RegisterUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    _, token = AuthToken.objects.create(user)

    send_verification_email(user.email, user.email_token)       

    return  Response({
        'user_info': {
        'id': user.id,
        'email': user.email,
        'email_token': user.email_token
        },
        'message': 'Account Created Successfully, Check Your Email to Activate your Account',
    })


@api_view(['POST'])
def signin(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    if user.is_verfied == False:
        return Response({
            'message': 'Please Acticate your account first, check your email'
        })
   

    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info': {
        'id': user.id,
        'email': user.email
        },
        'token': token
    })


@api_view(['GET'])
def verify_email(request, token):
    try:
        user = User.objects.get(email_token=token)
        if user.is_verfied:
            return Response({'message': 'email already verified'})
        
        user.is_verfied = True
        user.save() 
        return Response({'message': 'email verified successfully'})
    except Exception:
        return Response({'message': 'Invalid email token'})

    
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_user_data(request):
    serializer = UserSerializer(request.user)
    user = serializer.data
    
    return Response({
        "user_info": {
        "user_id": user['id'],
        "user_email": user['email'],
        "user_type": user['user_type'],
        }                     
    })


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_profile_avatar(request):
    data = request.data 
    user_id = request.user.id

    data["user"] = user_id
    serializer = UserAvatarSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Profile picture created successfuly", "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


