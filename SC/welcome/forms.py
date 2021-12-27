#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django import forms
from .models import Club, Project, Post


class SignupForm(UserCreationForm):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    sc_name = forms.CharField(label='Science Club Name', max_length=1000)
    phone_number = forms.CharField(validators=[phone_regex], max_length=17)
    email = forms.EmailField(required=True)

    class Meta:
        model = Club
        fields = ('username', 'sc_name', 'password1', 'password2', 'email', 'phone_number')

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.sc_name = self.cleaned_data['sc_name']
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']

        if commit:
            user.save()
        return user

    def is_valid(self):
        """Return True if the form has no errors, or False otherwise."""
        return self.is_bound, self.errors


class ScienceClubEditForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ["about", "email", "phone_number", "profile_image", "background_image"]


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'about', 'active', 'start_date', 'deadline', 'image']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'contents', 'image']












