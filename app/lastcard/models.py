import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        'username',
        max_length=150,
        blank=True,
        null=True,
    )

    mobile = models.CharField(max_length=31)
    company = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    birthday =  models.DateField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    social_profile = models.URLField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=datetime.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    card_url = models.URLField(null=True, blank=True)
    qr_code_url = models.URLField(null=True, blank=True)
    original_user = models.ForeignKey(User,on_delete=models.PROTECT, related_name="original_user")
    current_user = models.ForeignKey(User,on_delete=models.PROTECT, related_name="current_user", null=True, blank=True) # card holder


    def __str__(self):
        return str(self.id)


class CardUser(models.Model):
    card = models.ForeignKey(Card, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-created_at"]
