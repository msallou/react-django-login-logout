from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from user_profile.models import UserProfile
from .serializers import UserProfileSerializer


class GetUserProfileView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            username = user.username
            user = User.objects.get(id = user.id) # gets instance of user

            user_profile = UserProfile.objects.get(user=user)

            user_profile = UserProfileSerializer(user_profile)

            return Response({'profile': user_profile.data, 'username':str(username)})
        except:
            return Response({'error': 'something went wrong when retrieving profile'})

class UpdateUserProfileView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
            username = user.username
            
            data = self.request.data

            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']

            user = User.objects.get(id = user.id) # gets instance of user

            UserProfile.objects.filter(user=user).update(first_name=first_name, last_name=last_name, email=email)

            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)

            return Response({'profile': user_profile.data, 'username':str(username)})
        except:
            return Response({'error': 'something went wrong when updating profile'})