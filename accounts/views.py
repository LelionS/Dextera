from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def staff_required(user):
    return user.is_staff or user.is_superuser

@user_passes_test(staff_required)
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_staff = bool(request.POST.get('is_staff'))
        is_superuser = bool(request.POST.get('is_superuser'))

        if not username or not password:
            messages.error(request, 'Username and password are required.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()
            messages.success(request, 'User created successfully.')
            return redirect('user_management')

    return render(request, 'admin_panel/create_user.html')

@user_passes_test(staff_required)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.is_staff = bool(request.POST.get('is_staff'))
        user.is_superuser = bool(request.POST.get('is_superuser'))
        user.save()
        messages.success(request, 'User updated successfully.')
        return redirect('user_management')

    return render(request, 'admin_panel/edit_user.html', {'user': user})

@user_passes_test(staff_required)
def change_user_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('user_management')

    return render(request, 'admin_panel/change_password.html', {'user': user})


# accounts/views.py

from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.shortcuts import redirect

class RoleBasedLoginView(LoginView):
    template_name = 'accounts/login.html'  # same as before

    def get_success_url(self):
        user = self.request.user
        # Respect ?next= if it exists
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to

        # Role-based redirect
        if user.is_staff or user.is_superuser:
            return reverse('week_entries')
        return reverse('week_form')
