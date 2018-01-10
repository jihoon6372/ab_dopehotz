from django	import forms

class AgreeForm(forms.Form):
	i_agree = forms.BooleanField()