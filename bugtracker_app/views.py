from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# from bugtracker_main.settings import AUTH_USER_MODEL
from bugtracker_app import models, forms

 
@login_required
def index_view(request):
    tickets = models.Ticket.objects.all()
    new_tickets = tickets.filter(status="New").order_by("-date")
    in_progress_tickets = tickets.filter(status="In Progress")
    done_tickets = tickets.filter(status="Done")
    invalid_tickets = tickets.filter(status="Invalid")
    return render(
        request,
        "index.html",
        {
            "headline": "Bugtracker!",
            "new_tickets": new_tickets,
            "in_progress_tickets": in_progress_tickets,
            "done_tickets": done_tickets,
            "invalid_tickets": invalid_tickets,
        },
    )


@login_required
def add_ticket_form_view(request):
    if request.method == "POST":
        form = forms.TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            models.Ticket.objects.create(
                title=data.get("title"),
                description=data.get("description"),
                filed_by=request.user,
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = forms.TicketForm()
    return render(request, "generic_form.html", {"form": form})


@login_required
def ticket_detail_view(request, ticket_id):
    info = models.Ticket.objects.filter(id=ticket_id).first()
    return render(
        request, "ticket_detail.html", {"headline": "Ticket Detail!", "info": info}
    )


@login_required
def ticket_edit_view(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        form = forms.TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket.description = data["description"]
            ticket.title = data["title"]
            ticket.save()
        return HttpResponseRedirect(reverse("edit", args=[ticket_id]))

    data = {"title": ticket.title, "description": ticket.description}

    form = forms.TicketForm(initial=data)
    return render(request, "generic_form.html", {"form": form})


@login_required
def assign_action(request, ticket_id):
    edit = models.Ticket.objects.get(id=ticket_id)
    edit.status = "In Progress"
    edit.assigned_to = request.user
    edit.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def unassign_action(request, ticket_id):
    edit = models.Ticket.objects.get(id=ticket_id)
    edit.status = "New"
    edit.assigned_to = None
    edit.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def complete_action(request, ticket_id):
    edit = models.Ticket.objects.get(id=ticket_id)
    edit.status = "Done"
    edit.assigned_to = None
    edit.completed_by = request.user
    edit.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def reopen_action(request, ticket_id):
    edit = models.Ticket.objects.get(id=ticket_id)
    edit.status = "New"
    edit.assigned_to = None
    edit.completed_by = None
    edit.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def invalid_action(request, ticket_id):
    edit = models.Ticket.objects.get(id=ticket_id)
    edit.status = "Invalid"
    edit.assigned_to = None
    edit.completed_by = None
    edit.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def user_detail_view(request, user_id):
    current_user = models.MyUser.objects.filter(id=user_id).first()
    user_tickets = models.Ticket.objects.filter(filed_by=current_user)
    user_assigned = models.Ticket.objects.filter(assigned_to=current_user)
    user_completed = models.Ticket.objects.filter(completed_by=current_user)
    return render(
        request,
        "user_detail.html",
        {
            "headline": "User View!",
            "current_user": current_user,
            "user_tickets": user_tickets,
            "user_assigned": user_assigned,
            "user_completed": user_completed,
        },
    )


def login_view(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data.get("username"), password=data.get("password")
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get("next", reverse("homepage"))
                )

    form = forms.LoginForm()
    return render(
        request, "generic_form.html", {"headline": "Login : Bug Tracker!", "form": form}
    )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))
