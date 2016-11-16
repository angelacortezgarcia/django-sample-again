from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post

class ContactForm(forms.Form):
    full_name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField()

class PostForm(forms.ModelForm):
    content = forms. CharField(widget=PagedownWidget(show_preview=False))
    class Meta:
        model = Post
        fields = [
            "title",
            "image",
            "content",

        ]
