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
    ordering = ['title']
    actions = [booked]

    class Meta:
        model = Post

    def booked(self, request, queryset):
        rows_updated = queryset.update(status='b')
        if rows_updated ==1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully marked as booked." % message_bit)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "location", "bio", "birth_date", "company", "url"]

    class Meta:
        model = Profile


admin.site.register(Post, PostModelAdmin)

admin.site.register(Profile, ProfileAdmin)
