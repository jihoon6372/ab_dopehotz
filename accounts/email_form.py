from django	import forms
from .models import User
from django.utils.translation import gettext_lazy as _
policy_agree_errors = {
    'required': '이용약관은 필수 선택 항목입니다.'
}
privacy_agree_errors = {
    'required': '개인정보 취급방침은 필수 선택 항목입니다.'
}

class UserForm(forms.ModelForm):
	policy_agree = forms.BooleanField(error_messages=policy_agree_errors)
	privacy_agree = forms.BooleanField(error_messages=privacy_agree_errors)
	mailing_agree = forms.BooleanField(required=False)

	class Meta:
		model = User
		fields = ('email',)
			
		error_messages = {
            'email': {
                'required': '이메일을 입력해주세요.',
                'unique': '이미 가입 된 이메일입니다.',
                'invalid': '올바른 이메일 주소를 입력해주세요.',
            },
        }