from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from copy import deepcopy

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


rating_choices = [ (x, str(x)) for x in range(1, 6) ]
class RankForm(forms.Form):

    course = forms.CharField(max_length=30, required=True, help_text='Required')
    instructor = forms.CharField(max_length=30, required=True, help_text='Required')
    usefulness = forms.ChoiceField(deepcopy(rating_choices))
    lecture_quality = forms.ChoiceField(deepcopy(rating_choices))
    overall_quality = forms.ChoiceField(deepcopy(rating_choices))
    oral_written_tests_helpful = forms.ChoiceField(deepcopy(rating_choices))
    learned_much_info = forms.ChoiceField(deepcopy(rating_choices))

    def __init__(self, *args, **kwargs):
        super(RankForm, self).__init__(*args, **kwargs)

