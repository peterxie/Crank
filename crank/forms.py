from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password

from django.utils.translation import ugettext, ugettext_lazy as _

from .models import Course_Faculty_Table, Course_Listing_Table, Faculty_Table

from copy import deepcopy

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].help_text = "Must be a Columbia Uni"
        self.fields["password1"].help_text = "Required. must contain at least 8 characters"


class RankForm(forms.Form):

    course_faculty_pair = forms.ModelChoiceField(queryset=Course_Faculty_Table.objects.all().order_by('course'))

    rating_choices = [ (x, str(x)) for x in range(1, 6) ]
    usefulness = forms.ChoiceField(deepcopy(rating_choices), help_text='1(worst) - 5(best)')
    lecture_quality = forms.ChoiceField(deepcopy(rating_choices), help_text='1(worst) - 5(best)')
    overall_quality = forms.ChoiceField(deepcopy(rating_choices), help_text='1(worst) - 5(best)')
    oral_written_tests_helpful = forms.ChoiceField(deepcopy(rating_choices), help_text='1(worst) - 5(best)')
    learned_much_info = forms.ChoiceField(deepcopy(rating_choices), help_text='1(worst) - 5(best)')

    def __init__(self, *args, **kwargs):
        super(RankForm, self).__init__(*args, **kwargs)

class ChangePasswordForm(forms.Form):

    error_messages = {
        'password_mismatch':_("The two password fields didn't match."),
        'incorrect_password':_("The old password is invalid!"),
        'same_as_old_password':_("new password is the same as the old password!"),
    }
    old_password = forms.CharField(label=_("Old Password"), widget=forms.PasswordInput)
    new_password1 = forms.CharField(label=_("New Password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("Confirm New Password"), 
                                    widget=forms.PasswordInput,
                                    help_text=_("Enter the same password as above, for verification"))

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        old_password = self.cleaned_data.get("old_password")
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return old_password, password2

    def save(self, username, old_password, new_password):
        user = User.objects.get(username=username) 
        if not check_password(old_password, user.password):
            raise forms.ValidationError(
                self.error_messages['incorrect_password'],
                code='incorrect_password',
            )

        if check_password(new_password, user.password):
            raise forms.ValidationError(
                self.error_messages['same_as_old_password'],
                code='same_as_old_password',
            )

        user.password = make_password(new_password)
        user.save(update_fields=["password"])
