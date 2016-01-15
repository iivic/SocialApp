from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import UserProfile, User
from .forms import ProfileForm, UserForm
from django.http import JsonResponse
from django.db.models import Q


@login_required
def user_profile(request):
    user = get_object_or_404(User, pk=request.user.pk)
    profile = get_object_or_404(UserProfile, user_id=request.user.pk)
    if request.method == 'POST':
        print request.FILES
        form_profile = ProfileForm(request.POST or None, request.FILES or None, prefix="form_account", instance=profile)
        form_account = UserForm(request.POST or None, prefix="form_user", instance=user)
        if form_account.is_valid() and form_profile.is_valid():
            form_account.save()
            form_profile.save()
            return redirect('posts:index')
        return render(request, "user_details/index.html", {'form_account': form_account,
                                                           'form_profile': form_profile,
                                                           'profile': profile, })
    else:
        form_profile = ProfileForm(instance=profile, prefix="form_account")
        form_account = UserForm(instance=user, prefix="form_user")

    return render(request, "user_details/index.html", {'form_account': form_account,
                                                       'form_profile': form_profile,
                                                       'profile': profile, })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
        return render(request, "user_details/change_password.html", {'form': form, })
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "user_details/change_password.html", {'form': form, })


@login_required
def show_friends(request):
    user_profile = get_object_or_404(UserProfile, user_id=request.user.pk)
    user_friends_list = user_profile.friends.all().exclude(pk=request.user.id).order_by("first_name")
    paginator = Paginator(user_friends_list, 2)  # show 1 posts per page
    page = request.GET.get('page')
    try:
        user_friends = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        user_friends = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page of results
        user_friends = paginator.page(paginator.num_pages)
    return render(request, "user_details/friend_list.html", {"user_friends": user_friends, })


@login_required
def search_friends(request):
    if request.method == "POST":
        search_input = request.POST['searchInput']
        current_user = get_object_or_404(UserProfile, user_id=request.user.id)
        friends = current_user.friends.filter(Q(first_name__icontains=search_input) |
                                              Q(last_name__icontains=search_input) |
                                              Q(username__icontains=search_input)).exclude(pk=request.user.id)
        sorted_friends = friends.order_by("first_name", "last_name", "username")
        # get all avatar urls from friend profile
        friends_profile_avatar = [friend.userprofile.avatar.url for friend in sorted_friends]
        # cant return queryset so we get dictionary and then a list
        friends_list = [friend for friend in sorted_friends.values()]

        return JsonResponse({"friends": friends_list, "friends_profile_avatar": friends_profile_avatar})


@login_required
def find_friends(request):
    if request.method == "POST":
        search_input = request.POST["search_input"]
        users_matched = User.objects.filter(Q(first_name__icontains=search_input) |
                                            Q(last_name__icontains=search_input) |
                                            Q(username__icontains=search_input))\
            .exclude(pk=request.user.id).order_by("first_name", "last_name", "username")
        users_matched_avatar = [user.userprofile.avatar.url for user in users_matched]
        users_matched = [user for user in users_matched.values()]
        current_user = get_object_or_404(UserProfile, user_id=request.user.id)
        current_user_friends = [friend["username"] for friend in current_user.friends.values()]
        return JsonResponse({"usersMatched": users_matched, "currentUserFriends": current_user_friends,
                             "usersMatchedAvatar": users_matched_avatar})

    return render(request, "user_details/search_friends.html", {})


@login_required
def edit_friendship(request):
    if request.method == "GET":
        action = request.GET["action"]
        friend_id = request.GET["friend_id"]
        friend = get_object_or_404(User, pk=friend_id)
        friend_name = friend.first_name.encode('utf8') + " " + friend.last_name.encode('utf8')
        if action == "add":
            # add selected friend as friend and add user as friend to selected friend
            request.user.userprofile.friends.add(friend)
            friend.userprofile.friends.add(request.user)
        elif action == "remove":
            # remove selected friend as friend and remove user as friend to selected friend
            request.user.userprofile.friends.remove(friend)
            friend.userprofile.friends.remove(request.user)

        return JsonResponse({"friendName": friend_name})

    return HttpResponse("Not a GET request")
