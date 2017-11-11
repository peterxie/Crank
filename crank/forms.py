from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

