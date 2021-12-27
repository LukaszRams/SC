from django.contrib import admin
from .models import Club, Post, Project


# Register your models here.

class PostInLine(admin.StackedInline):
    model = Post
    extra = 0
    readonly_fields = fields = ["title", "publication_date"]
    can_delete = False
    show_change_link = True


class ProjectInLine(admin.StackedInline):
    model = Project
    extra = 0
    readonly_fields = fields = ["title", "active", "start_date", "deadline"]
    can_delete = False
    show_change_link = True



@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['sc_name', 'is_active', 'date_joined']
    fields = ['username', 'sc_name', 'about', 'email', 'phone_number', "profile_image", "background_image", 'is_active', 'date_joined']
    search_fields = ['sc_name']
    list_filter = ['is_active', 'date_joined']
    readonly_fields = ['username', 'date_joined']
    inlines = [ProjectInLine, PostInLine]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "parent", "active", "start_date", "deadline"]
    fields = ["parent", "title", "about", "active", "image_tag", "start_date", "deadline"]
    search_fields = ['title']
    list_filter = ['active']
    readonly_fields = ['image_tag', "parent"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "parent", "publication_date"]
    fields = ["parent", "title", "contents", "image_tag", "publication_date"]
    search_fields = ['title', "contents"]
    list_filter = ["publication_date"]
    readonly_fields = ['image_tag', "parent", "publication_date"]





