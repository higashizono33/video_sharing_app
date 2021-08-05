from django.forms import ModelForm
from django import forms
from .models import Resident, Community, Video, VideoGroup
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder

class CommunityCreateForm(ModelForm):
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 3}))
    password = forms.CharField(label='password', max_length=100, widget=forms.TextInput(attrs={'type': 'password'}))

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
    url = forms.URLField(required=True, widget=forms.TextInput(attrs={'placeholder': 'YouTube link here'}))

    def __init__(self, *args, **kwargs):
        community_id = kwargs.pop('community_id')
        super(VideoCreateForm, self).__init__(*args, **kwargs)
        community = Community.objects.get(id=community_id)
        group_list = []
        groups = VideoGroup.objects.filter(community=community)
        for group in groups:
            group_list.append((group.id, group.name))

        self.fields['group'].choices = group_list
        self.fields['group'].label = 'Group *please use add-tab'

        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": '', "id":'community.id'}
        self.helper.layout = Layout(
            Row(
                Column('url', css_class='form-group col-md-6 mb-0'),
                Column('title', css_class='form-group col-md-6 mb-0'),
                css_class='row'
            ),
            Row(
                Column('group', css_class='form-group col-md-6 mb-0'),
                ButtonHolder(
                    Submit('submit', 'add', css_class='px-lg-5'),
                    css_class='form-group col-md-6 mb-0 text-start pt-4'
                ),
                css_class='row'
            ),
        )

    class Meta:
        model = Video
        fields = ['url', 'title', 'group']

class GroupCreateForm(ModelForm):
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 3}))
    
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
    password = forms.CharField(label='community-password', max_length=100, widget=forms.TextInput(attrs={'type': 'password'}))


