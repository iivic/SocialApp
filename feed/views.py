from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post, Comment, PostLike, CommentLike
from .forms import PostForm, CommentForm


@login_required
def index(request):
    post_list = Post.objects.order_by('-created_at')
    paginator = Paginator(post_list, 5)  # show 5 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page of results
        posts = paginator.page(paginator.num_pages)

    user_post_likes = []
    for post_like in PostLike.objects.filter(user_id=request.user.id):
        user_post_likes.append(post_like.post_id)
    return render(request, 'feed/index.html', {'posts': posts, 'user_post_likes': user_post_likes})


@login_required
def show(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment_set.order_by('created_at')
    user_post_likes = []
    user_comment_likes = []
    for post_like in PostLike.objects.filter(user_id=request.user.id):
        user_post_likes.append(post_like.post_id)
    for comment_like in CommentLike.objects.filter(user_id=request.user.id):
        user_comment_likes.append(comment_like.comment_id)

    # POST request
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = Comment(post_id=pk,
                                  user_id=request.user.id,
                                  content=comment_form.cleaned_data['content'], )
            new_comment.save()
            return redirect('posts:show', pk=pk)
    else:  # GET request
        comment_form = CommentForm()
    return render(request, 'feed/show.html', {'post': post, 'comments': comments,
                                              'comment_form': comment_form,
                                              'user_post_likes': user_post_likes,
                                              'user_comment_likes': user_comment_likes})


@login_required
def create(request):
    # POST request
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = Post(user_id=request.user.id,
                            title=form.cleaned_data['title'],
                            content=form.cleaned_data['content'], )
            new_post.save()
            return redirect('posts:index')
    else:  # GET request
        form = PostForm()
    return render(request, 'feed/new.html', {'form': form})


@login_required
def like(request):
    post_id = request.GET['post_id']
    post = get_object_or_404(Post, pk=post_id)
    post_likes = post.postlike_set
    num_likes = post_likes.count()
    status = 0  # post not liked

    # check if the user already liked this post
    if not post_likes.filter(user_id=request.user.id).exists():
        # store the like in the db
        post_like = PostLike(post_id=post_id, user_id=request.user.id)
        post_like.save()
        num_likes += 1
        status = 1  # post liked
    else:  # remove the like from the db
        post_likes.get(user_id=request.user.id).delete()
        num_likes -= 1
    return JsonResponse({'num_likes': num_likes, 'status': status})


@login_required
def update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # POST request
    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:  # GET request
        form = PostForm(instance=post)
    return render(request, 'feed/edit.html', {'form': form, 'pk': pk})


@login_required
def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post_id=pk)
    # delete all comment likes
    for comment in comments:
        CommentLike.objects.filter(comment_id=comment.id).delete()
    # delete all comments
    comments.delete()
    # delete all post likes
    PostLike.objects.filter(post_id=pk).delete()
    # delete the post
    post.delete()
    return redirect('posts:index')


@login_required
def like_comment(request):
    comment_id = request.GET['comment_id']
    comment = get_object_or_404(Comment, pk=comment_id)
    comment_likes = comment.commentlike_set
    num_likes = comment_likes.count()
    status = 0  # comment not liked

    # check if the user already liked this comment
    if not comment_likes.filter(user_id=request.user.id).exists():
        # store the like in the db
        comment_like = CommentLike(comment_id=comment_id, user_id=request.user.id)
        comment_like.save()
        num_likes += 1
        status = 1  # comment liked
    else:  # remove the like from the db
        comment_likes.get(user_id=request.user.id).delete()
        num_likes -= 1
    return JsonResponse({'num_likes': num_likes, 'status': status})


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = get_object_or_404(Post, pk=comment.post.id)
    # delete all comment likes
    CommentLike.objects.filter(comment_id=comment.id).delete()
    # delete the comment
    comment.delete()
    return redirect('posts:show', pk=post.id)
