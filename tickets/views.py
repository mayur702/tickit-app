from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, Comment
from tickets.forms import TicketForm, CommentForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

# List all tickets with optional filtering by status
@login_required
def ticket_list(request):
    status_filter = request.GET.get('status', None)
    
    print(status_filter)
    print("hello")
    if status_filter:
        tickets = Ticket.objects.filter(status=status_filter)
    else:
        tickets = Ticket.objects.all()
    
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

# Create a new ticket
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.creator = request.user  # Set the creator to the current user
            ticket.save()
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketForm()
    return render(request, 'tickets/create_ticket.html', {'form': form})


def ticket_detail(request, ticket_id):
    #Get the ticket object or return a 404 if not found
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    #Retrieve all comments related to the ticket
    comments = ticket.comments.all()

    #Initialize the comment form
    comment_form = CommentForm(request.POST or None)
    
    if request.method == 'POST' and comment_form.is_valid():
        #Create a new comment instance
        comment = comment_form.save(commit=False)
        comment.ticket = ticket  # Associate comment with the ticket
        comment.user = request.user  # Assign the current user as the commenter
        comment.save()
        return redirect('ticket_detail', ticket_id=ticket.id)
    
    # Render the template with ticket and comment data
    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
def update_ticket_status(request, ticket_id):
    """
    View for updating the status of a ticket.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Check if the user is allowed to update the status
    if request.user != ticket.assigned_engineer and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to update this ticket.")

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['New', 'In Progress', 'Resolved', 'Closed']:
            ticket.status = new_status
            ticket.save()
            return redirect('ticket_detail', ticket_id=ticket.id)  # Replace 'ticket_detail' with your detail view name

    return render(request, 'ticket_detail.html', {'ticket': ticket})

@login_required
def add_comment(request, ticket_id):
    """
    View for adding a comment to a ticket.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
            return redirect('ticket_detail', ticket_id=ticket.id)  # Replace 'ticket_detail' with your detail view name

    else:
        form = CommentForm()

    return render(request, 'ticket_detail.html', {'ticket': ticket, 'comment_form': form})