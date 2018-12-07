from django.shortcuts import render, get_object_or_404, redirect, Http404
from .models import article, author, category, comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import articleForm, registerForm, authorForm, commentForm, categoryForm
from django.contrib import messages


def index(request):
    posts = article.objects.all()
    search = request.GET.get('search')
    if search:
        posts = posts.filter(
            Q(title__icontains=search)|
            Q(body__icontains=search)
        )
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = { 'posts': total_article }
    return render(request, "index.html", context)

def getAuthor(request, name):
    post_author = get_object_or_404(User, username=name)
    auth = get_object_or_404(author, name=post_author.id)
    posts = article.objects.filter(article_author=auth.id)
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = { 'posts': total_article, 'auth': auth }
    return render(request, "user_posts.html", context)

def getSingle(request, id):
    post = get_object_or_404(article, pk=id)
    first = article.objects.first()
    last = article.objects.last()
    related = article.objects.filter(category=post.category).exclude(id=id)[:4]
    getcomment = comment.objects.filter(post=id)
    form = commentForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.post=post
        instance.save()
        messages.success(request, 'Comment Added Successfully')
    context = { 'post': post, 'first': first, 'last': last, 'related': related, 'form': form, 'comment': getcomment }
    return render(request, "single.html", context)

def getCategory(request, name):
    cat = get_object_or_404(category, name=name)
    posts = article.objects.filter(category=cat.id)
    context = { 'posts': posts, 'cat': cat }
    return render(request, "category.html", context)

def getCategories(request):
    categories = category.objects.all()
    context = { 'categories': categories }
    return render(request, "categories.html", context)

def getCreateCategory(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            form = categoryForm(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, 'Category Successfully Created.')
                return redirect('categories')
            context = { 'form': form }
            return render(request, 'create_category.html', context)
        else:
            raise Http404('You are not authorized to access this page')
    else:
        return redirect('login')

def getLogin(request):
    if request.user.is_authenticated:
        return redirect(index)
    else:
        if request.method == 'POST':
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, 'Username or Password Invalid.')
                return render(request, "login.html")
    return render(request, "login.html")


def getLogout(request):
    logout(request)
    return redirect('index')


def getCreate(request):
    if request.user.is_authenticated:
        a_u = get_object_or_404(author, name=request.user.id)
        form = articleForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author=a_u
            instance.save()
            messages.success(request, 'Article Successfully Created.')
            return redirect('index')
        context = { 'form': articleForm() }
        return render(request, 'create.html', context)
    else:
        return redirect('login')
        

def getUpdate(request, id):
    if request.user.is_authenticated:
        a_u = get_object_or_404(author, name=request.user.id)
        post = get_object_or_404(article, id=id)
        form = articleForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author=a_u
            instance.save()
            messages.success(request, 'Article Successfully Updated.')
            return redirect('profile')
        else:
            messages.success(request, 'Article Not Updated.')
            context = { 'form': form}
            return render(request, 'create.html', context)
    else:
        return redirect('login')


def getDelete(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(article, id=id)
        post.delete()
        messages.success(request, 'Article Successfully Deleted.')
        return redirect('profile')
    else:
        return redirect('login')
        

def getProfile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id) 
        author_profile = author.objects.filter(name=user.id)
        if author_profile:
           auth = get_object_or_404(author, name=request.user.id)
           posts = article.objects.filter(article_author=request.user.id)
           context = { 'posts': posts, 'auth': auth }
           return render(request, 'profile.html', context)
        else:
            form = authorForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name=user
                instance.save()
                messages.success(request, 'Author Successfully Created.')
                return redirect('profile')
            else:
                context = { 'form': form }
                return render(request, 'createauthor.html', context)
    else:
        return redirect('login')        


def getRegister(request):
    form = registerForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Registation Successfully Completed.')
        return redirect('login')
    else:
        context = { 'form': form}
        return render(request, 'register.html', context)
    

