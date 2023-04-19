from django.db import models
from django.db.models.deletion import SET_NULL
from django.contrib.auth import get_user_model
from instructor.models import Instructor

User = get_user_model()


class Section(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    instructors = models.ManyToManyField(
        Instructor, related_name='sections_teaching', blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.name


class Course(models.Model):

    TYPE = (
        ('paid', ('paid course')),
        ('free', ('free course')),
        ('private', ('private course')),
    )


    LANGUAGE = (
        ('arabic', ('arabic')),
        ('english', ('english')),
        ('mixed', ('mixed')),
    )

    LEVELS = (
        ('Alllevels', ('All levels')),
        ('Beginner', ('Beginner')),
        ('Intermediate', ('Intermediate')),
        ('Advanced', ('Advanced')),
    )

    STATUS = (
        ('published', ('published')),
        ('unpublished', ('unpublished')),
        ('pending', ('pending')),
    )


    name = models.CharField(max_length=50)
    brief = models.CharField(max_length=1000, null=True)
    description = models.TextField(max_length=3000, null=True)
    type = models.CharField(max_length=20,
                            choices=TYPE, default='free', verbose_name=("Type of Course"))
    language = models.CharField(max_length=20,
                            choices=LANGUAGE, default='arabic', verbose_name=("Language of Course"), null=True)
    sections = models.ManyToManyField(
        Section, related_name='courses')
    instructor = models.ForeignKey(
        Instructor, on_delete=SET_NULL, related_name='courses', null=True)
    contributors = models.ManyToManyField(
        Instructor, related_name='contributed_courses', blank=True)
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    discount_enabled = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    certified = models.BooleanField(default=False)
    certificate = models.BooleanField(default=False)
    level = models.CharField(max_length=20,
                            choices=LEVELS, default='all_levels', verbose_name=("Level of Course"))
    status = models.CharField(max_length=20,
                            choices=STATUS, default='unpublished', verbose_name=("Status of Course"))
    thumbnail = models.ImageField(upload_to="courses/thumbnail", null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    num_lectures = models.IntegerField(null=True, blank=True, default=0)
    duration = models.FloatField(null=True, blank=True, default=0)
    num_reviews = models.IntegerField(null=True, blank=True, default=0)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    total_rating = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)

    @property
    def is_paid(self):
        return self.type == 'paid'

    def __str__(self):
        return self.name


class CourseBenefit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='benefits')
    description = models.CharField(max_length=300)

class CourseFaq(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=1000)


class Chapter(models.Model):
    name = models.CharField(max_length=50)
    number = models.IntegerField(null=True, default=1)
    duration = models.FloatField(null=True, blank=True, default=0)
    num_lectures = models.IntegerField(null=True, blank=True, default=0)
    instructor = models.ForeignKey(
        Instructor, on_delete=SET_NULL, related_name='chapters', null=True)
    course = models.ForeignKey(
        Course, on_delete=SET_NULL,  related_name='chapters', null=True)

    class Meta:
        ordering = ['number']
        
    def __str__(self):
        return self.name




class CartItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='cart_items')

    def __str__(self):
        return self.course.name


# help fuction to define the location for uploaded lecture
def upload_to(instance, filename):
        return f'{instance.instructor}/{instance.chapter.course.name}/{instance.chapter}/{filename}'


class Lecture(models.Model):

    TYPE = (
        ('premium', ('premium lecture')),
        ('free', ('free lecture')),
    )

    title = models.CharField(max_length=50, null=True)
    number = models.IntegerField(null=True, blank=True, default=10)
    duration = models.FloatField(null=True, blank=True, default=0)
    convert_status = models.CharField(max_length=40, null=True, blank=True)
    type = models.CharField(max_length=20,
                            choices=TYPE, default='premium', verbose_name=("Type of Lecture"))
    # source = models.FileField(upload_to='new-lectures/', null=True)
    # source = models.FileField(upload_to=upload_to, null=True)
    source = models.CharField(max_length=400, null=True)
    key = models.CharField(max_length=300, null=True)
    aws_bucket_name = models.CharField(max_length=200, null=True, default='allemniy-main')
    aws_bucket_region = models.CharField(max_length=200, null=True, default='me-south-1')
    formatted_vid_bucket= models.CharField(max_length=200, null=True, blank=True)
    formatted_vid_key= models.CharField(max_length=200, null=True, blank=True)
    formatted_vid_url= models.CharField(max_length=200, null=True, blank=True)
    cloudfront_url = models.CharField(max_length=300, null=True, blank=True)
    chapter = models.ForeignKey(
        Chapter, related_name='lectures', on_delete=models.CASCADE)
    instructor = models.ForeignKey(
        Instructor, related_name='lectures', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['number']

    

    def __str__(self):
        return self.title


class LectureStatus(models.Model):
    lecture = models.ForeignKey(
        Lecture, related_name='statuses', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.lecture.title}-{self.user.email}"



class CourseReview(models.Model):
    course = models.ForeignKey(Course, related_name='reviews', on_delete=models.SET_NULL, null=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)


class PublicationRequest(models.Model):
    TYPE = (
        ('publish', ('publish')),
        ('unpublish', ('unpublish')),
    )
    course = models.ForeignKey(Course, related_name='publication_requests', on_delete=models.SET_NULL, null=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)
    is_handled = models.BooleanField(default=False)
    instructor_message = models.TextField(null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    reviewer_note = models.TextField(null=True, blank=True)
    reviewer_decision = models.CharField(max_length=20, choices=TYPE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    request_type = models.CharField(max_length=20,
                            choices=TYPE, default='publish', verbose_name=("Type of Request"))
    terms_accepted = models.BooleanField(null=True, blank=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.instructor.name
    
class EnrolledCourse(models.Model):
    METHODS = (
        ('buying', ('buying')),
        ('free', ('free')),
    )

    user = models.ForeignKey(User, related_name='enrolled_courses', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHODS, default='buying', verbose_name=("Method of Enrollmemt"))
    enrolled_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.course.name}"

    