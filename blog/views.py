from django.core import paginator
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.utils.text import slugify

from user_profile.models import User

from .models import (
    Blog,
    Category,
    Reply,
    Tag,
    Comment
)
from .forms import TextForm, AddBlogForm


def home(request):
    blogs = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    context = {
        "blogs": blogs,
        "tags": tags
    }
    return render(request, 'home.html', context)


def blogs(request):
    queryset = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 4)

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs": blogs,
        "tags": tags,
        "paginator": paginator
    }
    return render(request, 'blogs.html', context)


def category_blogs(request, slug):
    category = get_object_or_404(Category, slug=slug)
    queryset = category.category_blogs.all()
    tags = Tag.objects.order_by('-created_date')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 2)
    all_blogs = Blog.objects.order_by('-created_date')[:5]

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs": blogs,
        "tags": tags,
        "all_blogs": all_blogs
    }
    return render(request, 'category_blogs.html', context)


def tag_blogs(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    queryset = tag.tag_blogs.all()
    tags = Tag.objects.order_by('-created_date')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 2)
    all_blogs = Blog.objects.order_by('-created_date')[:5]

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs": blogs,
        "tags": tags,
        "all_blogs": all_blogs
    }
    return render(request, 'category_blogs.html', context)


def blog_details(request, slug):
    form = TextForm()
    blog = get_object_or_404(Blog, slug=slug)
    category = Category.objects.get(id=blog.category.id)
    related_blogs = category.category_blogs.all()
    tags = Tag.objects.order_by('-created_date')[:5]
    liked_by = request.user in blog.likes.all()

    if request.method == "POST" and request.user.is_authenticated:
        form = TextForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                blog=blog,
                text=form.cleaned_data.get('text')
            )
            return redirect('blog_details', slug=slug)

    context = {
        "blog": blog,
        "related_blogs": related_blogs,
        "tags": tags,
        "form": form,
        "liked_by": liked_by
    }
    return render(request, 'blog_details.html', context)
