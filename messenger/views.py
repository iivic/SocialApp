from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Conversation, Message
from .forms import ConversationForm, MessageForm


@login_required
def index(request):
    conversation_list = Conversation.objects.filter(participants__id=request.user.id)\
        .annotate(Max('message__created_at')).order_by('-message__created_at__max')
    paginator = Paginator(conversation_list, 5)  # show 5 conversations per page
    page = request.GET.get('page')
    try:
        conversations = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        conversations = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page of results
        conversations = paginator.page(paginator.num_pages)

    participants = {}
    for conversation in conversations:
        user_names = []
        for user in conversation.participants.order_by('first_name', 'last_name'):
            if user.id != request.user.id:
                user_names.append(user.get_full_name())
        participants[conversation.id] = user_names
    return render(request, 'messenger/index.html', {'conversations': conversations, 'participants': participants})


@login_required
def show(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    messages = conversation.message_set.order_by('-created_at')
    # POST request
    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            new_message = Message(conversation_id=pk,
                                  sender_id=request.user.id,
                                  content=form.cleaned_data['content'], )
            new_message.save()
            return redirect('messages:show', pk=pk)
    else:  # GET request
        form = MessageForm()

    user_names = []
    for user in conversation.participants.order_by('first_name', 'last_name'):
        if user.id != request.user.id:
            user_names.append(user.get_full_name())
    return render(request, 'messenger/show.html', {'conversation': conversation, 'user_names': user_names,
                                                   'messages': messages, 'form': form})


@login_required
def create(request):
    # POST request
    if request.method == 'POST':
        form = ConversationForm(request.user.id, data=request.POST)

        if form.is_valid():
            # create and save the Conversation object
            new_conversation = Conversation.objects.create(subject=form.cleaned_data['subject'])
            # add participants
            current_user = get_object_or_404(User, pk=request.user.id)
            new_conversation.participants.add(current_user)
            for participant in form.cleaned_data['participants']:
                new_conversation.participants.add(participant)
            # send first message
            first_message = Message(conversation_id=new_conversation.id,
                                    sender_id=request.user.id,
                                    content=form.cleaned_data['message'])
            first_message.save()
            return redirect('messages:show', pk=new_conversation.pk)
    else:  # GET request
        form = ConversationForm(request.user.id)
    return render(request, 'messenger/new.html', {'form': form})


@login_required
def delete(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    # delete all messages
    conversation.message_set.all().delete()
    # delete the conversation
    conversation.delete()
    return redirect('messages:index')
