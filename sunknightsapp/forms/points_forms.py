from django import forms

class PointSubmissionForm(forms.Form):
    points=forms.IntegerField(label='Points',min_value=0)