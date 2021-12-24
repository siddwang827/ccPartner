from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

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
            'hobby',
            'background',
            'job',
        ]
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            fields.widget.attrs.update({
                'class': 'input',
            })   
