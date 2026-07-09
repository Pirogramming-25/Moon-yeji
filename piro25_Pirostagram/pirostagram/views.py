from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Post, Like, Comment, Follow, Story, StoryImage
from .forms import PostForm, CommentForm


@login_required(login_url='pirostagram:login')
def home_view(request):
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    posts = Post.objects.filter(
        Q(author_id__in=following_ids) | Q(author=request.user)
    ).order_by('-created_at')
    liked_post_ids = set(
        Like.objects.filter(user=request.user, post__in=posts).values_list('post_id', flat=True)
    )
    stories_qs = Story.objects.filter(
        Q(author_id__in=following_ids) | Q(author=request.user)
    ).order_by('-created_at')

    seen_authors = set()
    stories = []
    for story in stories_qs:
        if story.author_id not in seen_authors:
            seen_authors.add(story.author_id)
            stories.append(story)

    return render(request, 'pirostagram/home.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids,
        'stories': stories,
    })


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pirostagram:home')
    else:
        form = UserCreationForm()
    return render(request, 'pirostagram/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pirostagram:home')
        else:
            messages.error(request, '아이디 또는 비밀번호가 틀렸습니다.')
    return render(request, 'pirostagram/login.html')


def logout_view(request):
    logout(request)
    return redirect('pirostagram:login')


@login_required(login_url='pirostagram:login')
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('pirostagram:home')
    else:
        form = PostForm()
    return render(request, 'pirostagram/post_form.html', {'form': form})


@login_required(login_url='pirostagram:login')
def post_edit_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('pirostagram:home')
    else:
        form = PostForm(instance=post)
    return render(request, 'pirostagram/post_form.html', {'form': form, 'is_edit': True})


@login_required(login_url='pirostagram:login')
def post_delete_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
    return redirect('pirostagram:home')


@login_required(login_url='pirostagram:login')
def post_like_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    like_count = post.likes.count()
    return JsonResponse({'liked': liked, 'like_count': like_count})


@login_required(login_url='pirostagram:login')
def comment_create_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('pirostagram:home')


@login_required(login_url='pirostagram:login')
def comment_edit_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
    return redirect('pirostagram:home')


@login_required(login_url='pirostagram:login')
def comment_delete_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        comment.delete()
    return redirect('pirostagram:home')


@login_required(login_url='pirostagram:login')
def user_search_view(request):
    query = request.GET.get('q', '')
    users = []
    if query:
        users = User.objects.filter(
            Q(username__icontains=query)
        ).exclude(id=request.user.id)
    return render(request, 'pirostagram/user_search.html', {'users': users, 'query': query})


@login_required(login_url='pirostagram:login')
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    follower_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    return render(request, 'pirostagram/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'follower_count': follower_count,
        'following_count': following_count,
    })


@login_required(login_url='pirostagram:login')
def follow_toggle_view(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return redirect('pirostagram:profile', username=username)

    follow, created = Follow.objects.get_or_create(
        follower=request.user, following=target_user
    )

    if not created:
        follow.delete()

    return redirect('pirostagram:profile', username=username)


@login_required(login_url='pirostagram:login')
def story_create_view(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        if images:
            story = Story.objects.create(author=request.user)
            for order, image in enumerate(images):
                StoryImage.objects.create(story=story, image=image, order=order)
            return redirect('pirostagram:home')
    return render(request, 'pirostagram/story_form.html')


@login_required(login_url='pirostagram:login')
def story_view(request, username):
    story_user = get_object_or_404(User, username=username)
    user_stories = Story.objects.filter(author=story_user).order_by('created_at')
    images = StoryImage.objects.filter(story__in=user_stories).order_by('story__created_at', 'order')
    return render(request, 'pirostagram/story_view.html', {'story_user': story_user, 'images': images})