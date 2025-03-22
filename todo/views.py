from .forms import UserNameForm
from rest_framework import generics
from .models import User , Item
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .serializers import UserSerializer, ItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from todo.permissions import IsOwner
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import logout
from django.contrib import messages


def init(request):
    return render(request, 'todo/init.html')

def list(request, user):
    user = get_object_or_404(User, username=user)
    items = Item.objects.filter(user=user)
    return render(request, 'todo/list.html', {'items': items,'user': user})

def add_item(request, user):
    user = get_object_or_404(User, username=user)
    if request.method == 'POST':
        item_text = request.POST.get('inputString')
        if item_text:
            user.add_item(item_text=item_text)  
        return redirect('todo:list', user=user) 
    return render(request, "todo/add_item.html" , {'user': user})

def toggle_status(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    STATUS_CYCLE = ['not done', 'in progress', 'review', 'done']
    current_index = STATUS_CYCLE.index(item.status)
    next_index = (current_index + 1) % len(STATUS_CYCLE)  # Loop back to start after last status
    item.status = STATUS_CYCLE[next_index]
    item.save()

    return redirect('todo:list', user=item.user.username)

class ItemList(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)  
    
class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)  

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET','POST'])
def signup_user(request):
    error_message = None  
    if request.accepted_renderer.format == 'json':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'POST':
        form = UserNameForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            
            if User.objects.filter(username=user).exists():
                error_message = "This username has already been taken.Please login."
            else:
                User.objects.create(username=user)
                return render(request, 'todo/success.html', {'user': user})
    else:
        form = UserNameForm()
    return render(request, 'todo/signup.html', {'form': form, 'error_message': error_message})

@api_view(['GET','POST'])
def login_user(request):
    error_message = None  
    if request.accepted_renderer.format == 'json':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'POST':
        form = UserNameForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            if User.objects.filter(username=user).exists():
                return render(request, 'todo/success.html', {'user': user})
            else:
                error_message = "This user doesn't exist. Please signup."
    else:
        form = UserNameForm()   
    return render(request, 'todo/login.html', {'form': form , 'error_message': error_message})

@api_view(['POST'])
def logout_user(request):
    error_message = None
    
    try:
       request.user.auth_token.delete()
    except AttributeError:
        pass

    logout(request)
    if request.accepted_renderer.format == 'json':
        return Response({"message": "Successfully logged out and token deleted"}, status=status.HTTP_200_OK)

    messages.success(request, "You have been logged out successfully.")
    return redirect('todo:login')


# class UserSignupView(generics.CreateAPIView):
#     serializer_class = UserSerializer

# class UserLoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key})
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

# class UserLogoutView(APIView):
#     # authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request):
#         request.user.auth_token.delete()
#         return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    