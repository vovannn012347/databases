from django import forms

class LoginForm(forms.Form):
    username     = forms.CharField(label='username',  required=True, max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    username    = forms.CharField(label='username')
    password    = forms.CharField(widget=forms.PasswordInput(), label='password')
    password2   = forms.CharField(widget=forms.PasswordInput(),label='repeat password')
    email       = forms.CharField(label='email')
    description = forms.CharField(label='about self', widget=forms.Textarea, required=False)

class UploadBookForm(forms.Form):
    name            = forms.CharField(label='name',         required=True, max_length=255)
    description     = forms.CharField(label='description',  widget=forms.Textarea, required=False)
    author          = forms.CharField(label='author',       required=False)
    rate            = forms.ChoiceField(label='rate',       required=False,
                                        choices=(('1', '1'),('2','2'),('3','3'),('4','4'),('5','5')))
    image           = forms.FileField(required = False)
    bookFile        = forms.FileField(required = False)
