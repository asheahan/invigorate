from django.contrib import admin

# Register your models here.
from .models import Concept

class ConceptAdmin(admin.ModelAdmin):
    list_display = ('category', 'label',)
    list_display_links = ('label',)
    list_filter = ('category',)
    ordering = ('category', 'label',)
    search_fields = ('label',)

admin.site.register(Concept, ConceptAdmin)