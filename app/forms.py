from django.forms import ModelForm
from django import forms
from .models import Resident, Community, Video, VideoGroup

class CommunityCreateForm(ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description', 'password']

class ResidentCreateForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        self.logged_user = user
        super(ResidentCreateForm, self).__init__(*args, **kwargs)
        community_list = []
        communities = Community.objects.filter(owner=self.logged_user)
        for community in communities:
            community_list.append((community.id, community.name))

        self.fields['community'].choices = community_list
    
    class Meta:
        model = Resident
        fields = ['name', 'community']

class VideoCreateForm(ModelForm):
    
    class Meta:
        model = Video
        fields = ['url', 'title', 'group']

class GroupCreateForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        self.logged_user = user
        super(GroupCreateForm, self).__init__(*args, **kwargs)
        community_list = []
        communities = Community.objects.filter(owner=self.logged_user)
        for community in communities:
            community_list.append((community.id, community.name))

        self.fields['community'].choices = community_list

    class Meta:
        model = VideoGroup
        fields = ['name', 'community','description']

class ResidentLoginForm(forms.Form):
    name = forms.CharField(label='username', max_length=50)
    password = forms.CharField(label='password', max_length=100)


