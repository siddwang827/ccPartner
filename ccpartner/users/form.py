from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Hobby, Message

class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 
            'email', 
            'username', 
            'password1',
            'password2'
        ]

        labels = {
            'first_name':"Name"
        }

    # for CSS Styling

    def __init__(self, *args, **kwargs):
        super(CustomerUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name',
            'username',
            'email',
            'bio',
            'location',
            'profile_image',
            'social_facebook',
            'background',
            'job',
        ]
        widgets = {
            'profile_image': forms.FileInput,
        }
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            fields.widget.attrs.update({
                'class': 'input',
            })   


class HobbyForm(ModelForm):
    class Meta:
        model = Hobby
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(HobbyForm, self).__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            fields.widget.attrs.update({
                'class': 'input',
            })   


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = [
            'name',
            'email',
            'subject',
            'body'
        ]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
