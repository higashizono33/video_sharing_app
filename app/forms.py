from django.forms import ModelForm
from .models import Resident, Community, Video

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
        fields = ['url', 'title']

class ResidentAddForm(ModelForm):
    
    class Meta:
        model = Video
        fields = ['url', 'title']

