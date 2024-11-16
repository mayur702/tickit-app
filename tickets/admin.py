from django.contrib import admin
from .models import Ticket, Comment

# Ticket Model Admin Customization
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'assigned_engineer', 'status', 'created_at')  # Fields to display in the list view
    list_filter = ('status', 'creator', 'assigned_engineer')  # Filters to add to the right sidebar in the list view
    search_fields = ('title', 'description', 'creator__username', 'assigned_engineer__username')  # Fields to search in the admin
    ordering = ('-created_at',)  # Default ordering (most recent tickets first)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'created_at')  # Fields to display in the list view
    list_filter = ('ticket', 'user')  # Filters to add to the right sidebar in the list view
    search_fields = ('comment_text', 'ticket__title', 'user__username')  # Fields to search in the admin

# Register the models with custom admin options
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Comment, CommentAdmin)
