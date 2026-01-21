from django.shortcuts import render, redirect
from datetime import datetime

from accounts.models import User, Session
from accounts.decorator import login_required


def register(request):
    errors = []

    if request.method == "POST":
        form_data = request.POST

        username = form_data.get("username").strip()
        email = form_data.get("email").strip()
        password = form_data.get("password")
        password_confirm = form_data.get("password_confirm")

        print("Username: ", username)
        print("Email: ", email)
        print("Password: ", password)
        print("Confirm passowrd: ", password_confirm)

        if not username:
            errors.append("Enter the username")
        if not email:
            errors.append("Enter the email")
        if not password:
            errors.append("Enter the password")
        if password != password_confirm:
            errors.append("Passwords are not the same")
        if len(password) < 4:
            errors.append("Password must contain more than 4 characters")

        if User.objects.filter(username=username).exists():
            errors.append("User with this username already exists")
        if User.objects.filter(email=email).exists():
            errors.append("User with this email already exists")

        if not errors:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()

            return redirect("profile")


    return render(request, "accounts/register.html", { "errors": errors })


def login(request):
    errors = []

    if request.method == "POST":
        form_data = request.POST

        username = form_data.get("username").strip()
        password = form_data.get("password")

        if not username or not password:
            errors.append("Fill out all fields")
        else:
            try:
                user = User.objects.get(username=username)
                print("User password from DB: ", user.password)

                if user.check_password(password):
                    session = Session.create_session(user=user)
                    request._new_session = session

                    return redirect("profile")
                else:
                    errors.append("Username or password is not valid")
            except User.DoesNotExist:
                errors.append("This user doesn not exist")


    return render(request, "accounts/login.html", { "errors": errors })


def logout(request):
    if request.simple_session:
        request.simple_session.delete()

    request._delete_session = True

    return redirect("login")


@login_required
def profile(request):
    return render(request, "accounts/profile.html", { "user": request.simple_user })


def home(request):
    return render(request, "accounts/home.html", { "user": request.simple_user })