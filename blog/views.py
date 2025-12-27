from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from .forms import BlogForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Home / index
def index(request):
    return redirect('blog_list')  # redirect to blog list

# Blog CRUD views
def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog_list.html', {'blogs': blogs})  

@login_required
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_edit(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'blog_confirm_delete.html', {'blog': blog})

# Authentication views
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Signup successful!')
            return redirect('blog_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('blog_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('index')
