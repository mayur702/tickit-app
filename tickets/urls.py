from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('view/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('update/<int:ticket_id>/status/', views.update_ticket_status, name='update_ticket_status'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),

    path('ticket/<int:ticket_id>/update_status/', views.update_ticket_status, name='update_ticket_status'),
    path('ticket/<int:ticket_id>/add_comment/', views.add_comment, name='add_comment'),

    #path('login/', LoginView.as_view(), name='login'),
]
