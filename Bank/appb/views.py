from django.shortcuts import render
from rest_framework.views import APIView
from .models import BankDetailModel,User
from .serializer import BankDetailSerializer,Userserializer
from rest_framework.response import Response
from rest_framework import generics,filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime

# Create your views here.


class BankDetailList(APIView):
    def get(self,request):
        user = BankDetailModel.objects.all()
        serializer = BankDetailSerializer(user,many=True)
        return Response(serializer.data)


class GetBankDetails(APIView):

    def get_object(self, pk):
        return BankDetailModel.objects.get(id=pk)


    def get(self, request, pk, format=None):
        bank = self.get_object(pk)
        serializer = BankDetailSerializer(bank)
        return Response(serializer.data)


class BankDetailsbyIFSC(generics.ListAPIView):
    queryset = BankDetailModel.objects.all()
    serializer_class = BankDetailSerializer
    filter_backends = [filters.SearchFilter]
    search_fields =['=ifsc']



class BankDetailsbyNameCity(generics.ListAPIView):
    queryset = BankDetailModel.objects.all()
    serializer_class = BankDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields =['branch','city']


'''authentication'''

class RegisterView(APIView):
    def post(self,request):
        serializer = Userserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!!!')
        
        payload = {
            'id' : user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret' , algorithm='HS256')
        
        response = Response ()

        response.set_cookie(key='jwt',value=token, httponly=True)

        response.data = {
            'jwt':token
        }

        return response
    

class UserView(APIView):

    def get(self,request):
        token = request.COOKIES.get('jwt') 

        if not token:
            raise AuthenticationFailed('Unauthenticated!!!')
        
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!!!')
        
        user = User.objects.filter(id = payload['id']).first()
        serializer = Userserializer(user)


        return Response(serializer.data)
    

class LogoutView(APIView):

    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data ={
            'message':'success'
        }

        return response



