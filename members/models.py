from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator

class MemberManager(BaseUserManager):
    def create_user(self, name, password=None, **extra_fields):
        if not name:
            raise ValueError("The Name field is required")
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, password, **extra_fields)

class Members(AbstractBaseUser, PermissionsMixin):
    name = models.TextField(primary_key=True, max_length=150, unique=True)
    email=models.TextField(unique=True)
    discord = models.TextField(unique=True, max_length=150)
    github = models.TextField(unique=True, max_length=150)
    group = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    year = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], default=1)
    points = models.BigIntegerField(default=0)
    mentor = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='mentees')
    mentee = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='mentors')
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    track=models.ForeignKey('curriculum.Tracks',on_delete=models.CASCADE, null=True, blank=True)
    pfp=models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='profile_pics/default.png')
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['discord', 'github', 'email', 'group']

    objects = MemberManager()

    def __str__(self):
        return self.name