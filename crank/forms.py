from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["password1"].help_text = "Required. must contain at least 8 characters"

class RankForm(forms.ModelForm):
	course_number = forms.CharField(max_length=30, required=True, help_text='Required')
	course_instructor = forms.CharField(max_length=30, required=True, help_text='Required')
	quality = forms.CharField(max_length=10)

	class Meta:
		model = Course
		fields = ('course_number', 'course_instructor', 'quality')

	def __init__(self, *args, **kwargs):
		super(RankForm, self).__init__(*args, **kwargs)