from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Idea, Inspiration, Concept, Profile

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('label', 'created_date')
    list_display_links = ('label',)
    ordering = ('created_date',)
    search_fields = ('label', 'description',)


class ConceptAdmin(admin.ModelAdmin):
    list_display = ('category', 'label',)
    list_display_links = ('label',)
    list_filter = ('category',)
    ordering = ('category', 'label',)
    search_fields = ('label',)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.register(Idea, IdeaAdmin)
admin.site.register(Concept, ConceptAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
