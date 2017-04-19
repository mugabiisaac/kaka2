from django import forms
from .models import User

from .models import Post
from .models import Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "image",
            "price",
            "description",
            "Quantity",
            
        ]



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('url', 'location', 'company')
