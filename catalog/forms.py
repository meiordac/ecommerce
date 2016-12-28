from django import forms
from .models import Comment
 #this import should already be at the top
class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size':'2','value':'1', 'class':'quantity', 'maxlength':'5'}), error_messages={'invalid':'Please enter a valid quantity.'}, min_value=1)
    product_slug = forms.CharField(widget=forms.HiddenInput())
# override the default __init__ so we can set the request
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)
# custom validation to check for cookies
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies must be enabled.")
        return self.cleaned_data

class CommentForm(forms.Form):
    text = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"}),
    )
    stars = forms.MultipleChoiceField(
        required=False,
        widget=forms.RadioSelect,
        choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),),
    )

    def save(self, commit=True):
        data = self.cleaned_data
        comment = Comment()
        comment.text = data['text']
        comment.stars = data['stars']
        # do custom stuff
        if commit:
            comment.save()
        return comment


