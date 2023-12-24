from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from user_profile.models import UserProfile
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import auth
from .serializers import UserSerializer


# check whether a user is authenticated
@method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        try:
            isAuthenticated = User.is_authenticated

            if isAuthenticated:
                return Response({'isAuthenticated': 'success'})
            else:
                return Response({'isAuthenticated': 'error'})
        except:
            return Response({'error': 'Something went wrong when checking authentication'})



# Sign Up view
@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, ) # people signing up do not need any permissions

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        re_password = data['re_password']
        try:
            if password == re_password:
                if User.objects.filter(username=username).exists():
                    return Response({'error': 'Username Already Exists'})
                else:
                    if len(password) < 6:
                        return Response({'error': 'Password must be at least 6 characters'})
                    else:
                        user = User.objects.create_user(username=username, password=password)
                        user.save()

                        user = User.objects.get(id=user.id)
                        user_profile = UserProfile(user=user, first_name=first_name, last_name=last_name, email=email)
                        user_profile.save()

                        return Response({'success', 'User created successfully'})
            else:
                return Response({'error': 'Passwords do not match'})
        except:
            return Response({'error': 'Something went wrong while registering'})

        

@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, ) # people loging in do not need any permissions

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']
        try:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return Response({'success': 'Successfully Authenticated', 'username':username})
            else:
                return Response({'error': 'Error authenticating'})
        except:
            return Response({'error': 'Something went wrong while logging in'})

# will automatically be CSRF protected if user is logged in
class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({'success': 'Logged Out'})
        except:
            return Response({'success': 'Something went wrong while loggint out'})


# when you dispatch the application, you will get a CSRF cookie
@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, ) # people signing up do not need any permissions

    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})
    

class DeleteAccountView(APIView):
    def delete(self, request, format=None):
        user = self.request.user

        try:
            user = User.objects.filter(id=user.id).delete()

            return Response({'success', 'User deleted successfuly'})
        except:
            return Response({'error': 'something went wrong while deleting user'})
        

class GetUsersView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(slef, request, format=None):
        users = User.objects.all()

        users = UserSerializer(users, many=True)

        return Response(users.data)