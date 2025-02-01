from django.shortcuts import render
from .forms import UserNameForm
from .models import UserName , Item
from django.shortcuts import get_object_or_404, render, redirect

def init(request):
    return render(request, 'todo/init.html')

def signup(request):
    error_message = None  # Initialize the variable
    if request.method == 'POST':
        form = UserNameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            if UserName.objects.filter(username=username).exists():
                error_message = "This username has already been taken.Please login."
            else:
                UserName.objects.create(username=username)
                return render(request, 'todo/success.html', {'username': username})
    else:
        form = UserNameForm()
    return render(request, 'todo/signup.html', {'form': form, 'error_message': error_message})

def login(request):
    error_message = None
    if request.method == 'POST':
        form = UserNameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if UserName.objects.filter(username=username).exists():
                return render(request, 'todo/success.html', {'username': username})
            else:
                error_message = "This username doesn't exist. Please signup."
    else:
        form = UserNameForm()
        username = None
    return render(request, 'todo/login.html', {'form': form , 'username': username , 'error_message': error_message})

def list(request , username):
    username = get_object_or_404(UserName, username=username)
    return render(request, 'todo/list.html', {'username': username })

def add_item(request , username):
    user = get_object_or_404(UserName, username=username)
    if request.method == 'POST':
        item_text = request.POST.get('inputString')
        if item_text:
            user.add_item(item_text=item_text)  # Calls the method defined earlier
        return redirect('todo:list', username=username)  # Redirect to the list page
    return render(request , "todo/add_item.html" , {'username': user })

def toggle_status(request , item_id):
    item = get_object_or_404( Item, id=item_id)
    item.is_done = not item.is_done
    item.save()
    return redirect('todo:list', username=item.username.username)
