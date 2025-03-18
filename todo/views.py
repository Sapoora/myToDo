from django.shortcuts import render
from .forms import UserNameForm
from rest_framework import generics
from .models import User , Item
from django.shortcuts import get_object_or_404, render, redirect
from .serializers import UserSerializer, ItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from todo.permissions import IsOwner
from rest_framework.views import APIView

def init(request):
    return render(request, 'todo/init.html')

def signup(request):
    error_message = None  # Initialize the variable
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

def login(request):
    error_message = None
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
        user = None
    return render(request, 'todo/login.html', {'form': form , 'user': user , 'error_message': error_message})

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


# @api_view(['GET'])
# def taskList(request):
#     items = Item.objects.all()
#     serializer = ItemSerializer(items, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def taskDetail(request, pk):
#     item = Item.objects.get(id=pk)
#     serializer = ItemSerializer(item, many=False)
#     return Response(serializer.data)

# @api_view(['POST'])
# def taskCreate(request):
#     serializer = ItemSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# @api_view(['POST'])
# def taskUpdate(request, pk):
#     item = Item.objects.get(id=pk)
#     serializer = ItemSerializer(instance=item, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# @api_view(['DELETE'])
# def taskDelete(request, pk):
#     item = Item.objects.get(id=pk)
#     item.delete()
#     return Response("Item deleted successfully")

# @api_view(['GET'])
# def userList(request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)
