from django.contrib import admin
from .models import Like, Post, Comment

# Register your models here.
class LikeAdmin(admin.ModelAdmin):
    """
    Like admin tabs
    """
    list_display = [
        'user', 'object_id', 'content_type', 'content_object'
        ]

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like, LikeAdmin)