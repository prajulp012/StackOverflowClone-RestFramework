from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from .models import Question,Answer
from .serializers import UserSerializer,QuestionSer,AnswerSer
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

class UserViewSet(viewsets.ViewSet):
    def create(self,request):
        ser = UserSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({'msg':'Created'})
        return Response(data=ser.errors)
    
class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSer
    queryset=Question.objects.all()
    # authentication_classes = [authentication.TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self,request):
        ser = QuestionSer(data=request.data)
        if ser.is_valid():
            ser.save(user=request.user)
            return Response(data=ser.data)
        return Response(data=ser.errors)
    
    # def list(self,request):
    #     ser = Question.objects.all().exclude(user=request.user)
    #     dser = QuestionSer(ser,many=True)
    
    def get_queryset(self):
        return Question.objects.all().exclude(user=self.request.user)
    
    @action(methods=["POST"],detail=True)
    def add_answer(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        quest = Question.objects.get(id=id)
        user = request.user
        ser = AnswerSer(data=request.data)
        if ser.is_valid():
            ser.save(user=user,question=quest)
            return Response(data=ser.data)
        return Response(data=ser.errors)
class AnswerView(viewsets.ModelViewSet):
    serializer_class = AnswerSer
    queryset = Answer.objects.all()
    # authentication_classes = [authentication.TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("method not allowded")  
    def list(self, request, *args, **kwargs):
        raise serializers.ValidationError("method not allowded") 
    def destroy(self, request, *args, **kwargs):
        object = self.get_object()
        if request.user == object.user:
            object.delete()
            return Response(data="deleted")
        else:
            return serializers.ValidationError("permission denied for this user")
       
    @action(methods=['POST'],detail=True)    
    def add_upvote(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        ans = Answer.objects.get(id=id)
        ans.upvote.add(request.user)
        return Response(data='Upvotted')