from django.core.exceptions import ValidationError
import uuid
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from datetime import timedelta
import secrets
from .validators import validate_phone_number

#signals to auto updated relationships.

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.CharField(max_length=50, unique=True, null=True )

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not self.organization:
            raise ValidationError('An organization owner must be associated with an organization.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Trigger model-level validation
        return super().save(*args, **kwargs)

class CustomUserManager(UserManager):
    '''Added Further Email Verification here and Email as username in Abstract User .'''
    def _create_user(self, email, password, **extra_fields):
        if not email: 
            raise ValueError("You have not provided a valid e-mail address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    """User can be Employee or Customer"""
    #state = USStateField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True,blank=False, null=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)  # First name is required
    last_name = models.CharField(max_length=30, blank=False, null=False)  
    phone_number = models.CharField(max_length=20, blank=False, null=False, validators=[validate_phone_number])
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email" #we are specifying what we want to use as a username, in this case the email field.
    EMAIL_FIELD = "email"    #need this to make the email field required to use as a username.
    REQUIRED_FIELDS = []

    def format_phone_number(self):
        cleaned_number = ''.join(filter(str.isdigit, self.phone_number))
        
        # Check if the cleaned number has a valid length
        if len(cleaned_number) == 10:  # Assuming it's a 10-digit phone number
            formatted_number = f'{cleaned_number[:3]}-{cleaned_number[3:6]}-{cleaned_number[6:]}'
            return formatted_number
        else:
            return "Invalid phone number"


class OrganizationOwner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

class Customer(models.Model):
    """ Customer-specific information """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)

class Employee(models.Model):
    """ Employee-specific information """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey(Organization,  on_delete=models.CASCADE, null=True)


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_code = models.CharField(max_length=10)
    expires_at = models.DateTimeField()
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @staticmethod
    def generate_reset_code():
        return secrets.token_urlsafe(6)  # Generates a more secure 6-character code

    @classmethod
    def create_reset_entry(cls, user):
        code = cls.generate_reset_code()
        expires_at = timezone.now() + timezone.timedelta(minutes=10)  # Code expires in 10 minutes
        return cls.objects.create(user=user, reset_code=code, expires_at=expires_at)




