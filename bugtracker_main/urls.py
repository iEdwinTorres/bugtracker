"""bugtracker_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bugtracker_app import views

urlpatterns = [
    path('', views.index_view, name="homepage"),
    path('ticketdetail/<int:ticket_id>/edit/', views.ticket_edit_view),
    path('ticketdetail/<int:ticket_id>/', views.ticket_detail_view, name="edit"),
    path('userdetail/<int:user_id>/', views.user_detail_view),
    path('assignaction/<int:ticket_id>/', views.assign_action),
    path('unassignaction/<int:ticket_id>/', views.unassign_action),
    path('completeaction/<int:ticket_id>/', views.complete_action),
    path('reopenaction/<int:ticket_id>/', views.reopen_action),
    path('invalidaction/<int:ticket_id>/', views.invalid_action),
    path('addticket/', views.add_ticket_form_view, name="addticket"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('admin/', admin.site.urls),
]
