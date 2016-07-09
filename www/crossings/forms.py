from django import forms


class CommentForm(forms.Form):
    crossingId = forms.IntegerField()
    # Note that the max_length below should be the same as we use in
    # www/crossings/templates/crossings/index.html
    text = forms.CharField(max_length=4000)
