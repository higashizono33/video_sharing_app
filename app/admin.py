from django.contrib import admin
from .models import Resident, Community, VideoGroup, Video, Post, Comment

class ResidentAdmin(admin.ModelAdmin):
    pass
class CommunityAdmin(admin.ModelAdmin):
    pass
class VideoGroupAdmin(admin.ModelAdmin):
    pass
class VideoAdmin(admin.ModelAdmin):
    pass
class PostAdmin(admin.ModelAdmin):
    pass
class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Resident, ResidentAdmin)
admin.site.register(Community, CommunityAdmin)
admin.site.register(VideoGroup, VideoGroupAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
