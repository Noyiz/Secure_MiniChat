from django.shortcuts import render, redirect
from django.db.models import Q
from .models import user
from django.shortcuts import HttpResponse

def showAll(request):
    users = user.objects.all()
    count = users.count()
    return render(request, "index.html", context={"users": users, "count": count})

def finduser(request):
        str = request.POST.get("str")
        users = user.objects.filter(
            Q(username__icontains=str) | Q(email__icontains=str)
        )
        count = users.count()
        return render(request, "index.html", context={"users": users, "count": count})


def adduser(request):
    if request.method == "GET":
        return render(request, "add.html")
    else:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user.objects.create( username=username, email=email, password=password)
        return redirect("index.html")
def update(request):
    if request.method == "GET":
        username = request.GET['update_username']
        users = user.objects.get(username=username)
        return render(request, "update.html", context={"user": users})
    else:
        update_username = request.POST.get("username")
        update_user = user.objects.get(username=update_username)
        update_username = request.POST.get("username")
        update_email = request.POST.get("email")
        update_password = request.POST.get("password")
        update_user.username = update_username
        update_user.email = update_email
        update_user.password = update_password
        update_user.save()
        return redirect("index.html")


