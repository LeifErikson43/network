import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse, request
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow

@csrf_exempt
def index(request):
    
    posts = Post.objects.all().order_by('-timestamp')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        'page_obj': page_obj
        })

@csrf_exempt
@login_required    
def posts(request):
    if request.method == "POST":
       
        user = request.user
        data = json.loads(request.body)
        post_txt = data.get("post_txt","")
        a_post = Post(
            poster=user,
            post_txt=post_txt,
        )
        a_post.save()
    return render(request, "network/index.html")

@csrf_exempt
@login_required
def post(request, post_id):
    
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        print(data)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def likes(request, post_id):
    if request.method == "PUT":
        post = Post.objects.get(pk=post_id)
        post.likers.add(request.user)
        post.num_likes += 1
        post.save()
        
        data = {
            'post_id': post.id,
            'value': post.likers.all().count()
        }
        return JsonResponse(data, safe=False)

@csrf_exempt
@login_required
def unlike(request, post_id):
    if request.method == "PUT":
        post = Post.objects.get(pk=post_id)
        post.likers.remove(request.user)
        post.num_likes -= 1
        post.save()
        
        data = {
            'post_id': post.id,
            'value': post.likers.all().count()
        }
        return JsonResponse(data, safe=False)
    

    

@login_required
def profile(request, poster_id):
    if request.method == "GET":
        person = User.objects.get(pk=poster_id)
        name = person.username
        person_posts = Post.objects.filter(poster=person).order_by('-timestamp')
        person_following = Follow.objects.filter(follower=person)
        person_followers = Follow.objects.filter(following=person)
        followers_count = person_followers.count()
        following_count = person_following.count()
        user_is_follower = False
        if request.user != person:
            person_not_user = True
        else:
            person_not_user = False
        
        for i in person_followers:
            print(i.follower)
            if request.user == i.follower:
                user_is_follower = True
                break
            else:
                user_is_follower = False
            
    return render(request, "network/profile.html", {
        "name": name,
        "poster_id": poster_id,
        "person_posts": person_posts,
        "followers_count": followers_count,
        "following_count": following_count,
        "person_not_user": person_not_user,
        "person_followers": person_followers,
        "person_following": person_following,
        "user_is_follower": user_is_follower,
    })
    
@csrf_exempt
@login_required
def unfollow(request, poster_id):
    if request.method == "PUT":
        Follow.objects.filter(follower_id=request.user, following_id=poster_id).delete()
        per = User.objects.get(pk=poster_id)
        person_follow = Follow.objects.filter(following=per)
        follow_count = person_follow.count()
        data = {
            'follow_count': follow_count,
        }
        return JsonResponse(data, safe=False)
    
@csrf_exempt
@login_required
def follow(request, poster_id):
    if request.method == "PUT":
        per = User.objects.get(pk=poster_id)
        newFollow = Follow.objects.create(follower=request.user, following=per)
        newFollow.save()
        person_follow = Follow.objects.filter(following=per)
        follow_count = person_follow.count()
        data = {
            'follow_count': follow_count,
        }
        return JsonResponse(data, safe=False)


@login_required
def following(request):
    follow_user = request.user
    follow_list = Follow.objects.filter(follower=follow_user).values('following_id')
    posts = Post.objects.filter(poster__in=follow_list).order_by('-timestamp')
    print(follow_list)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "follow_user": follow_user,
        "follow_list": follow_list,
        "posts": posts,
        "page_obj": page_obj,
    })

@csrf_exempt   
@login_required
def edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("post") is not None:
            post.post_txt = data["post"]
        post.save()
        return HttpResponse(status=204)
    
@csrf_exempt
@login_required
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    return HttpResponse(status=204)