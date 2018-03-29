from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from account.models import MyUser


class UserCreationForm(forms.ModelForm):
    last_name = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    nickname = forms.CharField(required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('stu_num', 'last_name', 'first_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    last_name = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    nickname = forms.CharField(required=False)
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('stu_num', 'password', 'last_name', 'first_name',)

    def clean_password(self):
        return self.initial["password"]


class UserUpdateForm(forms.ModelForm):
    last_name = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    nickname = forms.CharField(required=False)

    class Meta:
        model = MyUser
        fields = ('last_name', 'first_name', 'nickname')
