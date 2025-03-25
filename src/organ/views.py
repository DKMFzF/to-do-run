from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (  # noqa: E501
    CustomAuthenticationForm,
    RegisterForm,
    TaskForm,
    TaskStatusForm,
)
from .models import Tasks


@login_required
def tasks(request):
    if request.method == "POST":
        if "title" in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
        elif "task_id" in request.POST:
            task = Tasks.objects.get(
                id=request.POST.get("task_id"), user=request.user
            )  # noqa: E501
            form = TaskStatusForm(request.POST, instance=task)
            if form.is_valid():
                task = form.save(commit=False)
                if task.statuss:
                    task.time_finish = datetime.now()
                else:
                    task.time_finish = None
                task.save()
        return redirect("tasks")
    tasks = Tasks.objects.filter(user=request.user)
    return render(
        request, "organ/tasks.html", {"tasks": tasks, "form": TaskForm()}
    )  # noqa: E501


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Tasks, id=task_id, user=request.user)
    task.delete()
    return redirect("tasks")


@login_required
def account(request):
    return render(request, "organ/account.html")


def calendar(request):
    tasks = Tasks.objects.all()
    return render(request, "organ/calendar.html", {"tasks": tasks})


def about(request):
    return render(request, "organ/about.html")


# def account(request):
#     return render(request, 'organ/account.html')


def home(request):
    return render(request, "organ/index.html")


def auth_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("account")
    else:
        form = CustomAuthenticationForm()
    return render(request, "organ/auth_login.html", {"form": form})


def auth_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("account")
    else:
        form = RegisterForm()
    return render(request, "organ/auth_register.html", {"form": form})


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect("home")
    return redirect("account")
