from django.contrib import admin

# Register your models here.
from .models import Post, Profile

def booked(modeladmin, request, queryset):
    queryset.update(status='k')
booked.short_description = "mark slelcted post as booked"


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "updated", "timestamp", "get_status_display"]
    list_display_links = ["updated"]
    list_editable = ["title"]
    list_filter = ["updated", "timestamp"]

    search_fields = ["title", "content"]

    class Meta:
        model = Post

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "location", "bio", "birth_date", "company", "url"]

    class Meta:
        model = Profile


admin.site.register(Post, PostModelAdmin)

admin.site.register(Profile, ProfileAdmin)
