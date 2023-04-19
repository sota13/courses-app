from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()




class UserProfile(models.Model):
    """non-auth-related/cosmetic fields"""

    GENDER = (
        ('male', ('male')),
        ('female', ('female')),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(
        max_length=30, default='first_name', null=True, blank=True)
    last_name = models.CharField(
        max_length=150, default='last_name', null=True, blank=True)
    is_instructor = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=18, null=True, blank=True)
    gender = models.CharField(
        max_length=6, choices=GENDER, default='male', null=True)
    bio = models.TextField(max_length=3000, null=True, blank=True,
                           default="I'm good at teaching many courses for example I teach...")

    @property
    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return ""

    def __str__(self):
        return self.user.email




"""receivers to add a User Profile for newly created users"""


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()



