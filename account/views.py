from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


class UserRegistrationForm(UserCreationForm):
    Meta = UserCreationForm.Meta
    Meta.fields = ('username', 'email')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            return render(request, 'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

        return render(request, 'registration/register.html',
                      {'user_form': user_form})


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'registration/edit.html', {'user_form': user_form})
