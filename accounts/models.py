from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):	
    def create_user(self, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('first name'), max_length=255, blank=True)
    soundcloud_url = models.CharField('사운드클라우드 URL', max_length=255, blank=True)
    profile_picture = models.CharField('프로필 이미지 URL', max_length=255, blank=True)
    greeting = models.TextField('인사말', blank=True)
    likes_greeting = models.TextField('좋아요 인사말', blank=True)
    clips_greeting = models.TextField('구독 인사말', blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    # is_block = models.BooleanField('블락여부', default=False, help_text="사용자 블락처리 할때 선택")
    mailing_agree = models.BooleanField('메일 수신여부', default=False, help_text='광고성 메일 수신 동의 여부')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name_plural = '사용자 계정'
        ordering = ['-date_joined']
            

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return self.username

    def get_short_name(self):
        "Returns the short name for the user."
        return self.username

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_profile(self):
        """
        Returns site-specific profile for this user. Raises
        SiteProfileNotAvailable if this site does not allow profiles.
        """
        warnings.warn("The use of AUTH_PROFILE_MODULE to define user profiles"
                      " has been deprecated.",
            PendingDeprecationWarning)
        if not hasattr(self, '_profile_cache'):
            from django.conf import settings
            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable(
                    'You need to set AUTH_PROFILE_MODULE in your project '
                    'settings')
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable(
                    'app_label and model_name should be separated by a dot in '
                    'the AUTH_PROFILE_MODULE setting')
            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable(
                        'Unable to load the profile model, check '
                        'AUTH_PROFILE_MODULE in your project settings')
                self._profile_cache = model._default_manager.using(
                                   self._state.db).get(user__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache


class DeleteUser(models.Model):
    user = models.ForeignKey(User, related_name='delete_social_auth', on_delete=models.CASCADE)
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    delete_date = models.DateTimeField(auto_created=True, auto_now=True, verbose_name='삭제일')

    class Meta:
        verbose_name_plural = '삭제된 계정'
        ordering = ['-delete_date']

    def __str__(self):
        return self.user.email
        


class AuthLog(models.Model):
    class Meta:
        verbose_name_plural = '로그인 기록'

    user = models.ForeignKey(User, null=True, verbose_name = '로그인 계정', on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=512, null=True)
    user_agent = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=50, default='success')
    auth_date = models.DateTimeField('접속일', auto_now_add=True)

    def __str__(self):
        return self.user.email
        

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)





from allauth.socialaccount.signals import social_account_updated, pre_social_login, social_account_removed
from allauth.account.signals import user_signed_up

@receiver(user_signed_up)
def user_signed_up_populate_user(sender, request, sociallogin, **kwargs):
    account = sociallogin.account
    data = account.extra_data
    user = account.user

    if 'kakao' in account.provider:
        user.username = data['properties']['nickname']

    if 'naver' in account.provider:
        user.username = data.get('name', data['nickname'])     

    if 'facebook' in account.provider:
        user.username = data.get('name', '')
        
    user.save()
    


@receiver(social_account_updated)
def social_account_updated_populate_user(sender, request, sociallogin, **kwargs):
    account = sociallogin.account
    data = account.extra_data
    user = account.user

    if 'kakao' in account.provider:
        user.username = data['properties']['nickname']
        user.profile_picture = data['properties']['profile_image']

    if 'naver' in account.provider:
        user.username = data.get('name', data['nickname'])
        user.profile_picture = data['profile_image']

    if 'facebook' in account.provider:
        user.username = data['name']
        

    user.save()


@receiver(pre_social_login)
def pre_social_login(sender, request, sociallogin, **kwargs):
    request.session['uid'] = sociallogin.account.uid



# @receiver(social_account_removed)
# def unlink_social_user(sender, request, sociallogin, **kwargs):
#     print('')
#     print('')
#     print('')
#     print(sociallogin.account.__dict__)
#     print('')
#     print('')
#     print('')