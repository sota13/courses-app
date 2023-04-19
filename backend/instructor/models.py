from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class Instructor(models.Model):
    STATUS = (
        ('listed', ('listed')),
        ('unlisted', ('unlisted')),
        ('pending', ('pending')),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=30, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    approved = models.BooleanField(default=False)
    request_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    num_reviews = models.IntegerField(null=True, blank=True, default=0)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    listing_status = models.CharField(max_length=20,
                            choices=STATUS, default='unlisted', verbose_name=("Status of Listing"))

    @property
    def name(self):
        return f"{self.user.userprofile.first_name}  {self.user.userprofile.last_name}"
    
    @property
    def profile(self):
        return self.user.userprofile

    def __str__(self):
        return f"{self.user.userprofile.first_name}  {self.user.userprofile.last_name}"


class InstructorRequest(models.Model):
    DECISION = (
        ('approved', ('approved')),
        ('rejected', ('rejected')),
    )
    instructor = models.OneToOneField(Instructor, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)
    is_handled = models.BooleanField(default=False)
    requested_date = models.DateTimeField(auto_now_add=True)
    handled_date = models.DateTimeField(auto_now=True)
    decision = models.CharField(max_length=20, choices=DECISION, null=True, blank=True)

    def __str__(self):
        return self.instructor.user.email




class InstructorReview(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)


class InstructorEducation(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, related_name='education')
    institution = models.CharField(max_length=100, null=True, blank=True)
    detail = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return str(self.institution)

class InstructorSkill(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, related_name='skills')
    name = models.CharField(max_length=100, null=True, blank=True)
    level = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.name)


class ContactItem(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class SocialMediaItem(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class InstructorContactInfo(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, related_name='contact_info')
    contact_item = models.ForeignKey(ContactItem, on_delete=models.CASCADE, null=True, related_name='instructors')
    detail = models.CharField(max_length=100, null=True, blank=True)
    show = models.BooleanField(null=True, blank=True, default=True)

    def __str__(self):
        return str(self.contact_item.name)

class InstructorSocialMedia(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, related_name='social_media')
    social_item = models.ForeignKey(SocialMediaItem, on_delete=models.CASCADE, null=True, related_name='instructors')
    link = models.CharField(max_length=100, null=True, blank=True)
    show = models.BooleanField(null=True, blank=True, default=True)

    def __str__(self):
        return str(self.social_item.name)
    
class ListingRequest(models.Model):
    TYPE = (
        ('list', ('list')),
        ('unlist', ('unlist')),
    )
    instructor = models.ForeignKey(Instructor, related_name='listing_requests', on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)
    is_handled = models.BooleanField(default=False)
    instructor_message = models.TextField(null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    reviewer_note = models.TextField(null=True, blank=True)
    reviewer_decision = models.CharField(max_length=20, choices=TYPE, null=True, blank=True)
    request_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    request_type = models.CharField(max_length=20,
                            choices=TYPE, default='list', verbose_name=("Type of Request"))
    terms_accepted = models.BooleanField(null=True, blank=True)

    class Meta:
        ordering = ['-request_date']

    def __str__(self):
        return self.instructor.name
    