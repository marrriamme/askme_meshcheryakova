from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile, Question, Tag, Answer

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        return self.cleaned_data['username'].lower().strip()
    

class SignupForm(forms.ModelForm):
    nickname = forms.CharField(required=True, label="NickName")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Repeat Password")
    avatar = forms.ImageField(required=False, label="Upload Avatar")
    email = forms.EmailField(required=True, label="Email Adress")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirmation'):
            self.add_error('password_confirmation', "Passwords do not match.")
        return cleaned_data    
    
    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email
    
    def clean_nickname(self):
        nickname = self.cleaned_data['nickname'].strip()
        if Profile.objects.filter(nickname=nickname).exists():
            raise ValidationError("This nickname is already in use.")
        return nickname

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)  
            profile.nickname = self.cleaned_data.get('nickname')
            profile.avatar = self.cleaned_data.get('avatar')
            profile.save()
        return user

    
class SettingsForm(forms.ModelForm):
    nickname = forms.CharField(required=False, label="NickName")  
    avatar = forms.ImageField(required=False, label="Upload Avatar")  
    email = forms.EmailField(required=False, label="Email Adress")

    class Meta:
        model = User  
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)  
        super().__init__(*args, **kwargs)
        if self.profile:  
            self.fields['nickname'].initial = self.profile.nickname
            self.fields['avatar'].initial = self.profile.avatar

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)  
        if commit:
            user.save()
            if self.profile:
                self.profile.nickname = self.cleaned_data.get('nickname', self.profile.nickname)
                self.profile.avatar = self.cleaned_data.get('avatar', self.profile.avatar)
                self.profile.save()
        return user


class AskForm(forms.ModelForm):
    title = forms.CharField(required=True, label="Title")
    text = forms.CharField(widget=forms.Textarea, required=True, label="Text")
    tags = forms.CharField(required=False, label="Tags") 

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        tag_list = [tag.strip() for tag in tags.split(',')] if tags else []

        if len(tag_list) > 3:
            raise ValidationError("You can only add up to 3 tags.")
        return tag_list
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError("The title must be at least 5 characters long.")
        return title

    def save(self, commit=True):
        question = super().save(commit=False)
        if commit:
            question.save()

        tag_list = self.cleaned_data['tags']
        
        for tag_name in tag_list:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            question.tags.add(tag)  

        return question

class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=True, label="Text")

    class Meta:
        model = Answer
        fields = ('text',)

    def save(self, commit=True):
        answer = super().save(commit=False)
        if commit:
            answer.save()

        return answer