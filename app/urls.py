from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('select_community', SelectCommunityView.as_view(), name='select_community'),
    path('create_community', CommunityCreateView.as_view(), name='create_community'),
    path('create_resident', ResidentCreateView.as_view(), name='create_resident'),
    path('add', AddView.as_view(), name='add'),
    path('add_community', add_community, name='add_community'),
    path('add_group', add_group, name='add_group'),
    path('home/community/<int:community_id>', HomeView.as_view(), name='home'),
    path('video/<int:pk>', VideoDetailView.as_view(), name='video'),
    path('comment/<int:post_id>', reply_comment, name='reply_comment'),
    path('add_like/<int:pk>', add_like, name='add_like'),
    path('remove_like/<int:pk>', remove_like, name='remove_like'),
    path('resident_login/<int:community_id>', ResidentLoginView.as_view(), name='resident_login'),
    path('resident_logout', resident_logout, name='resident_logout'),
    path('manage_resident', ManageResidentView.as_view(), name='manage_resident'),
    path('delete_resident/<int:resident_id>', delete_resident, name='delete_resident'),
    path('set_admin/<int:resident_id>', set_admin, name='set_admin'),
]