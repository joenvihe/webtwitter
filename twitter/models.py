from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import re
from urllib.parse import urlencode

# Create your models here.
class Tweet(models.Model):
    def __unicode__(self):
        return self.contenido
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    fecha = models.DateTimeField()
    contenido = models.CharField(max_length = 140)
    retweet = models.BooleanField(default = False, blank = True)
    activo = models.BooleanField(default  =True)
    respuesta = models.IntegerField(null = True, blank = True)
    def filtrar(self):
        """Filtra XSS enlaza hashtags, menciones y enlaces """
        t = self.contenido

        #Anti XSS
        t = t.replace('&','&amp;')
        t = t.replace('<','&lt;')
        t = t.replace('>','&gt;')
        t = t.replace('\'','&#39;')
        t = t.replace('"','&quot;')

        links = re.findall('http\\:\\/\\/[^ ]+', t)
        for link in links:
            t = t.replace(link, '<a href="%s">%s</a>' % (link, link))

        menciones = re.findall('\\@[a-zA-Z0-9_]+', t)
        for mencion in menciones:
            t = t.replace(mencion, '<a href="/twitter/profile/%s/">%s</a>' % (mencion[1:], mencion))

        return t


class Profile(models.Model):
    def __unicode__(self):
        return str(self.user)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    frase = models.CharField(max_length = 160)
    ubicacion = models.CharField(max_length = 50)
    avatar = models.CharField(max_length = 256)
    logo = models.FileField(null=True,blank=True,default='default.jpg')

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])