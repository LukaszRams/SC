from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, ProjectForm, PostForm, ScienceClubEditForm
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import Club, Project, Post, User
from django.utils import timezone
from django.conf import settings
from sms import send_sms
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from . import utils


# Basic views
def welcomeView(request):
    """
    Render first page view
    """
    return render(request, "welcome/index.html")


def home(request):
    """
    Render page with all clubs
    """
    clubs = Club.objects.all()
    return render(request=request, template_name='welcome/home.html', context={"clubs": clubs})


# Authentications views
def signup(request):
    """
    This view allowed to register new user
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        valid = form.is_valid()  # valid method has been overwritten to return errors
        if valid[0] and not list(valid[1].values()):
            form.save()
            messages.success(request, "Registration successful.")
            return redirect("signin")  # redirect to signin
        else:
            for error in list(valid[1].values())[0]:
                messages.error(request, error)
    # render view
    form = SignupForm()
    return render(
        request=request,
        template_name='welcome/accounts/signup.html',
        context={'form': form}
    )


def signin(request):
    """
    Signin user
    """
    # check if login button was pressed
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        # check if data is valid
        if form.is_valid():

            # extract username and password
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # authenticate the user
            user = authenticate(username=username, password=password)
            if user is not None:

                # login user and send message after it
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")

                # get next page
                next_page = request.POST.get("next")

                # checking if there is a next page (there is when we try to do something that requires login so
                # we are redirected to the login page. We want to log in and continue something)
                if next_page:
                    return redirect(next_page)

                # redirect to welcome window
                return redirect('welcome')
            else:
                # if something gone wrong, display error message
                messages.error(request, "Invalid username or password.")
        else:
            # if form is not valid
            messages.error(request, "Invalid username or password.")

    # render view
    form = AuthenticationForm()
    return render(
        request=request,
        template_name='welcome/accounts/signin.html',
        context={"form": form})


@login_required
def logout_request(request):
    """
    Logout the user
    It not render any view but redirect to welcome page
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("welcome")


@login_required
def deleteAccount(request, pk):
    """
    Logout the curent user and delete the accounts
    """
    logout(request)
    user = User.objects.get(pk=pk)
    name = Club.objects.get(pk=pk).sc_name

    # email to the user
    from_email = settings.EMAIL_HOST_USER
    subject = "Account deletion"
    email_to = Club.objects.get(pk=pk).email

    # creating email body
    context = {
        "name": Club.objects.get(pk=pk).sc_name,
    }

    # rendering template
    temp = get_template("welcome/emails/account_deleted.html")
    content = temp.render(context)

    user.delete()

    # send sms to the user
    send_sms(
        'Profile for ' + context["name"] + ' has been deleted',
        settings.TWILIO_NUMBER,
        [settings.TWILIO_TRIAL_NUMBER],
        fail_silently=False
    )

    # send email
    utils.send_html_mail(subject, content, [email_to], from_email)

    messages.success(request=request, message="Account for " + name + " has been deleted")
    return redirect("adeletes", name=name)


def adeletes(request, name):
    """
    a-delete-s  ( after-delete-successful )
    Show view with options after delete accounts
    """
    return render(request=request, template_name="welcome/profile/adeletes.html", context={"name": name})


# Password views
@login_required
def change_password(request):
    """
    Allows you to change the password of the current user
    """
    if request.method == 'POST':

        # fill the form
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():

            # save the data
            user = form.save()
            update_session_auth_hash(request, user)  # Important!

            # message succes and redirect
            messages.success(request, 'Your password has been changed')
            return redirect('welcome')
        else:
            messages.error(request, 'Please correct the error below.')

    # render the form
    form = PasswordChangeForm(request.user)
    return render(request, 'welcome/accounts/change_password.html', {
        'form': form
    })


# Profile manage functions
def profile(request, pk):
    """
    Render profile view and allowed to apply to the curent science club
    """

    # check if appy form was submited
    if request.method == "POST":
        # email to the science club
        email_from = settings.EMAIL_HOST_USER
        subject = 'Application from ' + request.POST["first_name"] + " " + request.POST["surname"]
        email_to = Club.objects.get(pk=pk).email

        # creating email body
        context = {
            "title": "Application to the science club",
            "content": request.POST["about"],
            "author": request.POST["first_name"] + " " + request.POST["surname"],
            "phone_number": request.POST["phone_number"],
            "email_address": request.POST["email"]
        }

        # rendering template
        temp = get_template("welcome/emails/apply_email_sc_side.html")
        content = body = temp.render(context)

        # check for resume
        if "cv" in request.FILES.keys():
            attachement = request.FILES["cv"]
        else:
            attachement = None

        # send amail in thread
        utils.send_html_mail(subject, content, [email_to], email_from, attachement)

        # email to the candidate
        from_email = settings.EMAIL_HOST_USER
        subject = 'Application to the ' + Club.objects.get(pk=pk).sc_name
        email_to = request.POST["email"]

        # creating email body
        context = {
            "title": "Application to the science club",
            "author": Club.objects.get(pk=pk).sc_name,
            "profile_id": pk
        }

        # rendering template
        temp = get_template("welcome/emails/apply_email_candidate_side.html")
        content = temp.render(context)

        # send amail in thread
        utils.send_html_mail(subject, content, [email_to], from_email)
        return redirect("profile", pk=pk)

    # get profile data
    profile = Club.objects.get(pk=pk)

    # get all projects, sort it, and check if it is a list format
    projects = Project.objects.order_by("-active", "start_date", "id").filter(parent_id=pk)
    if projects and type(projects) != list:
        projects = list(projects)

    # get all posts, sort it, and check if it is a list format
    posts = Post.objects.order_by("-publication_date").filter(parent_id=pk)
    if posts and type(posts) != list:
        posts = list(posts)

    # render profile
    context = {"profile": profile,
               "projects": projects,
               "posts": posts}
    return render(request=request, template_name="welcome/profile/profile.html", context=context)


@login_required
def editAccount(request, pk):
    # check if edit was clicked
    if request.method == "POST":

        # get club data
        club = Club.objects.get(pk=pk)

        # fill the form with data and files
        form = ScienceClubEditForm(request.POST, request.FILES, instance=club)

        # check if form is valid
        if form.is_valid():
            # the old file is deleted thanks to the plugin

            # the `form.save` will also update newest image & path.
            form.save()

            # send message and redirect
            messages.success(request=request, message="Profile has been edited succesfully")
            return redirect('profile', pk=pk)

    # render the edit view
    profile = Club.objects.get(pk=pk)
    return render(
        request=request,
        template_name='welcome/profile/editProfile.html',
        context={'profile': profile}
    )


# manage project functions
@login_required
def deleteProject(request, pk):
    """
    Delete project with specific pk (id)
    """
    prof_num = Project.objects.get(pk=pk).parent.id
    Project.objects.get(pk=pk).delete()

    # show message and redirect
    messages.success(request, "Project has been deleted")
    return redirect('profile', prof_num)


@login_required
def editProject(request, pk):
    """
    Render the project edit view
    """
    # check if edit button was clicked
    if request.method == "POST":

        # get project
        project = Project.objects.get(pk=pk)

        # fill the form
        form = ProjectForm(request.POST, request.FILES, instance=project)

        # check if form is valid
        if form.is_valid():
            # the old file is deleted thanks to the plugin

            # check if dates are correct
            if form.cleaned_data["start_date"] > form.cleaned_data["deadline"]:
                messages.error(request=request, message="Deadine is before start date !!!")
            else:
                # the `form.save` will also update your newest image & path.
                form.save()

                # show message and redirect
                messages.success(request=request, message="Project has been edited succesfully")
                return redirect('profile', pk=Project.objects.get(pk=pk).parent.id)

    # render view
    project = Project.objects.get(pk=pk)
    return render(
        request=request,
        template_name='welcome/profile/project/updateProject.html',
        context={'project': project}
    )


@login_required
def addProject(request, pk):
    """
    It allowed to add new project assigned to the science club
    """
    # check if add button was clicked
    if request.method == 'POST':
        # create project for science club
        project = Project(parent=Club.objects.get(pk=pk))

        # fill the form
        form = ProjectForm(request.POST, request.FILES, instance=project)

        # check if form is valid
        if form.is_valid():
            form.save()

            # show message and redirect
            messages.success(request, "Project successfuly added.")
            return redirect("profile", pk=pk)

    # render the view
    return render(
        request=request,
        template_name='welcome/profile/project/addProject.html'
    )


# manage post functions
@login_required
def deletePost(request, pk):
    """
    Delete posty with specific pk (id)
    """
    prof_num = Post.objects.get(pk=pk).parent.id
    Post.objects.get(pk=pk).delete()

    # show message and redirect
    messages.success(request, "Post has been deleted")
    return redirect('profile', prof_num)


@login_required
def editPost(request, pk):
    """
    Render the post edit view
    """
    # check if edit button was clicked
    if request.method == "POST":

        # get post
        post = Post.objects.get(pk=pk)

        # fill the form
        form = PostForm(request.POST, request.FILES, instance=post)

        # check if data is valid
        if form.is_valid():
            # the old file is deleted thanks to the plugin

            # the `form.save` will also update your newest image & path.
            form.save()

            # show message and redirect
            messages.success(request=request, message="Post has been edited succesfully")
            return redirect('profile', pk=Post.objects.get(pk=pk).parent.id)

    # render view
    post = Post.objects.get(pk=pk)
    return render(
        request=request,
        template_name='welcome/profile/post/updatePost.html',
        context={'post': post}
    )


@login_required
def addPost(request, pk):
    """
    It allowed to add new post assigned to the science club
    """
    # check if add button was clicked
    if request.method == 'POST':

        # create post for science club
        post = Post(parent=Club.objects.get(pk=pk), publication_date=timezone.now())

        # fill the form
        form = PostForm(request.POST, request.FILES, instance=post)

        # check if form is valid
        if form.is_valid():
            form.save()

            # show message and redirect
            messages.success(request, "Post successfuly added.")
            return redirect("profile", pk=pk)

    # render the view
    return render(
        request=request,
        template_name='welcome/profile/post/addPost.html'
    )


def reset_password(request):
    """
    Allows you to reset your password if you know your username and token
    """
    # check id=f post method
    if request.method == 'POST':
        # get and check user
        user = utils.check_if_user_exist(request.POST['username'])
        if user and user.token:

            # check passwords
            password1 = request.POST['password']
            password2 = request.POST['password2']
            invalid = True
            if password1 == password2:
                try:
                    invalid = validate_password(password1, user)
                except ValidationError as e:
                    messages.error(request=request, message=e)

            if not invalid:

                # check tokens
                if request.POST['token'] == user.token:
                    user.set_password(password1)
                    user.token = ""
                    user.save()

                    # send mail
                    # TODO: Create message template
                    subject = "Change of user password"
                    email_to = user.email
                    from_email = settings.EMAIL_HOST_USER

                    # creating email body
                    context = {
                        "sc_name": user.sc_name
                    }

                    # rendering template
                    temp = get_template("welcome/emails/password_reset.html")
                    content = temp.render(context)

                    # send email
                    utils.send_html_mail(subject, content, [email_to], from_email)

                    messages.success(request, "The new password has been saved")

                    return redirect("signin")  # redirect to signin
                else:
                    messages.debug(request=request, message="The token is invalid, maybe it has a space at the end")
        else:
            # If the user does not exist or does not have a generated token
            messages.error(request=request, message="Username is incorrect")

    # render view
    return render(
        request=request,
        template_name="welcome/accounts/reset_password.html"
    )


def generate_token(request):
    """
    Generate a password reset token and send it to the email address assigned to the user
    """
    # check if user submit
    if request.method == "POST":

        # check if user exist or show message
        user = utils.check_if_user_exist(username=request.POST["username"])

        # user exist
        if user:

            # generete token
            token = PasswordResetTokenGenerator()
            token = token.make_token(user)

            # save token
            user.token = token
            user.save()

            # send mail
            # TODO: Create message template
            subject = "Account token"
            email_to = user.email
            from_email = settings.EMAIL_HOST_USER

            # creating email body
            context = {
                "sc_name": user.sc_name,
                "token": token
            }

            # rendering template
            temp = get_template("welcome/emails/password_reset_token.html")
            content = temp.render(context)

            # send email
            utils.send_html_mail(subject, content, [email_to], from_email)

            # show message
            messages.info(request=request, message="Check your mail for more information")
            return redirect("home")

        # user not exist
        else:
            messages.error(request=request, message="Username is incorrect")

    # render view
    return render(
        request=request,
        template_name="welcome/accounts/generate_token.html"
    )
