from django import forms
from django.contrib.auth.models import User
from .models import Message


class UserMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class ConversationForm(forms.Form):
    def __init__(self, user_id, *args, **kwargs):
        super(ConversationForm, self).__init__(*args, **kwargs)
        self.fields['participants'].queryset = User.objects.exclude(id=user_id)
    subject = forms.CharField(max_length=255)
    participants = UserMultipleChoiceField(queryset=User.objects.all())
    message = forms.CharField(widget=forms.Textarea)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', ]
