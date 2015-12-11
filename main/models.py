from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
# Create your models here.


class Permission():
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENT = 0x08
    ADMINISTER = 0x80


class Role(models.Model):
    name = models.CharField(max_length=64)
    default = models.BooleanField(default=False)
    permission = models.IntegerField(null=True)

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENT, False),
            'Administrator': (Permission.ADMINISTER, False)
        }
        for r in roles:
            role = Role.objects.filter(name=r).first()
            if not role:
                role = Role(name=r)
            role.permission = roles[r][0]
            role.default = roles[r][1]
            role.save()

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address.')

        user = self.model(
            email=self.normalize_email(email),
            username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('User must have an email address.')

        user = self.create_user(
            username='admin', email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    # username, password, email
    email = models.EmailField(max_length=64, blank=True, unique=True)
    username = models.CharField(max_length=30)
    date_of_birth = models.DateField(default=timezone.now)
    last_seen = models.DateField(default=timezone.now)
    realname = models.CharField(max_length=64, null=True)
    location = models.CharField(max_length=64, null=True)
    about_me = models.TextField(null=True)
    role = models.ForeignKey(Role, default=2)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def can(self, permissions):
        return (self.role.permission & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    # Refresh the last_seen
    def ping(self):
        self.last_seen = timezone.now()
        self.save()