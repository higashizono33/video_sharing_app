from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('select_community', SelectCommunityView.as_view(), name='select_community'),
    path('create_community', CommunityCreateView.as_view(), name='create_community'),
    path('create_resident', ResidentCreateView.as_view(), name='create_resident'),
    path('add', AddView.as_view(), name='add'),
    path('add_community', add_community, name='add_community'),
    path('home/community/<int:community_id>', HomeView.as_view(), name='home'),
]