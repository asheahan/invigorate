from django.contrib import admin

# Register your models here.
from .models import Idea, Inspiration, Concept

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

admin.site.register(Idea, IdeaAdmin)
admin.site.register(Concept, ConceptAdmin)