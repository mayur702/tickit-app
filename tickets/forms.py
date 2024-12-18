from django import forms
from .models import Ticket, Comment

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'assigned_engineer', 'status']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
