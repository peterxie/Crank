from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError

from django.utils.translation import ugettext, ugettext_lazy as _

from .models import Course_Faculty_Table, Course_Listing_Table, Faculty_Table

from copy import deepcopy

"""
This class leverages the UserCreationForm so that when we invoke save, an object 
will be automatically saved in our database. This class is an instantiation of
our sign up form which will be used for registering for the site.
"""
class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Enter Username', min_length=6, max_length=7)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )
    
	#Initial vals that describe restrictions on username and passwords
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].help_text = "Must be a Columbia Uni"
        self.fields["password1"].help_text = "Required. must contain at least 8 characters"

	# Enforces uni length 6 or 7. The Proper uni format is xxxnnnn or xxnnnn,
	# where x is a character and n is a number.
    def clean_username(self):
        alpha = "abcdefghijklmnopqrstuvwxyz"
        num = "0123456789"
        username = self.cleaned_data['username'].lower()
        if len(username) == 6:
            if (username[0] not in alpha) or (username[1] not in alpha):
                raise ValidationError("Invalid uni format")
            for n in range (2, 6):
                if (username[n] not in num):
                    raise ValidationError("Invalid uni format")
        elif len(username) == 7:
            if (username[0] not in alpha) or (username[1] not in alpha) or (username[2] not in alpha):
                raise ValidationError("Invalid uni format")
            for n in range (3, 7):
                if (username[n] not in num):
                    raise ValidationError("Invalid uni format")
        else:
            raise ValidationError("Invalid uni format")
        return username

"""
This class encompasses the data needed to submit a rating. It allows us to create the fields and
ranges of values for a user to enter.
"""
class RankForm(forms.Form):

	#Populates forms with Course Faculty Pairings.
    course_faculty_pair = forms.ModelChoiceField(queryset=Course_Faculty_Table.objects.all().order_by('course'))

	#Creates a list 1 to 5 for the user to rate a field below.
    rating_choices = [ (x, str(x)) for x in range(1, 6) ]
    usefulness = forms.ChoiceField(deepcopy(rating_choices), help_text='1(worst) - 5(best)')
    lecture_quality = forms.ChoiceField(deepcopy(rating_choices), help_text='1(worst) - 5(best)')
    overall_quality = forms.ChoiceField(deepcopy(rating_choices), help_text='1(worst) - 5(best)')
    oral_written_tests_helpful = forms.ChoiceField(deepcopy(rating_choices), help_text='1(worst) - 5(best)')
    learned_much_info = forms.ChoiceField(deepcopy(rating_choices), help_text='1(worst) - 5(best)')

    def __init__(self, *args, **kwargs):
        super(RankForm, self).__init__(*args, **kwargs)

"""
This class encompasses the data needed to submit a rating. It allows us to create the fields and
ranges of values for a user to enter.
"""
class ChangePasswordForm(forms.Form):

    error_messages = {
        'password_mismatch':_("The two password fields didn't match."),
        'incorrect_password':_("The old password is invalid!"),
        'same_as_old_password':_("new password is the same as the old password!"),
		'incorrect_length':_("New password must be at least 8 characters."),
    }
    old_password  = forms.CharField(label=_("Old Password"), widget=forms.PasswordInput)
    new_password1 = forms.CharField(label=_("New Password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("Confirm New Password"), 
                                    widget=forms.PasswordInput,
                                    help_text=_("Enter the same password as above, for verification"))

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

	#Just make sure password1 and password2 match and prevents SQL injection via Django API.
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

	#Update user's new password in database
    def save(self, username, old_password, new_password):
        user = User.objects.get(username=username)

		#Make sure the old password matches so we allow changing password
        if not check_password(old_password, user.password):
            raise forms.ValidationError(
                self.error_messages['incorrect_password'],
                code='incorrect_password',
            )
		#Make sure new and old password don't match
        if check_password(new_password, user.password):
            raise forms.ValidationError(
                self.error_messages['same_as_old_password'],
                code='same_as_old_password',
            )
		#Make sure new password is greater than 8 chars
        if len(new_password) < 8:
            raise forms.ValidationError(
		self.error_messages['incorrect_length'],
                code='incorrect_length',
            )
        user.password = make_password(new_password)
        user.save(update_fields=["password"])

"""
This class encompasses the data needed to search for ratings.
"""
class SearchForm(forms.Form):
    course = forms.CharField(label=_("Course Number"), required=False, help_text="e.g. COMS W4156,4156")
    faculty = forms.CharField(label=_("Faculty Name"), required=False, help_text="e.g. Kaiser, Gail E")

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
