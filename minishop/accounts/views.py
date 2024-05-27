from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
import uuid

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if the email exists in the database
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address')
            return redirect('forgot_password')

        # Generate a token for password reset
        token = default_token_generator.make_token(user)

        # Create a password reset link
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri(reverse('reset_password')) + f'?uidb64={uidb64}&token={token}'

        # Send the password reset email
        subject = 'Reset Your Password'
        message = render_to_string('reset_password_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        send_mail(subject, message, None, [user.email])

        messages.success(request, 'An email with instructions to reset your password has been sent to your email address.')
        return redirect('forgot_password')

    return render(request, 'forgot_password.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes

def reset_password(request):
    if request.method == 'GET':
        # Get UIDb64 and token from query parameters
        uidb64 = request.GET.get('uidb64')
        token = request.GET.get('token')

        # Decode UIDb64 to user ID
        try:
            uid = urlsafe_base64_decode(uidb64).decode('utf-8')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Validate the token
        if user is not None and default_token_generator.check_token(user, token):
            # Token is valid, render the password reset form
            return auth_views.PasswordResetConfirmView.as_view(
                template_name='reset_password.html',
                success_url=reverse('password_reset_complete')
            )(request, uidb64=uidb64, token=token)
        else:
            # Invalid token or user not found, display an error message
            messages.error(request, 'The password reset link is invalid or has expired.')
            return redirect('forgot_password')

    elif request.method == 'POST':
        # This block handles the form submission for resetting the password
        return auth_views.PasswordResetConfirmView.as_view(
            template_name='reset_password.html',
            success_url=reverse('password_reset_complete')
        )(request)

    else:
        # Method not allowed
        return HttpResponse(status=405)



def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "*username is already taken")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "*email is already taken")
                return redirect("register")
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                #User is a keyword
                user.save()
                print("user created")
        else:
            print("*password is not matching")
            return redirect('register')

        return redirect('/')   # '/' is used to redirect to home
    else:
        return render(request,'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        print(user)

        if user is not None:
            auth.login(request, user)
            uid = str(uuid.uuid4())       #Generate a random UID
            request.session['uid'] = uid   #Add UID to the session
            request.session['username'] = username       #Adding username to session
            return redirect('/')
        else:
            messages.info(request,'*invalid USERNAME/PASSWORD entered')
            return redirect('login')

    else:
        return render(request, 'login.html')



def logout(request):
    auth.logout(request)
    return redirect('/')

