from django.contrib import admin
from .models import (Section, 
                     Course, 
                     Chapter, 
                     Lecture, 
                     LectureStatus, 
                     CourseReview, 
                     CourseBenefit, 
                     CourseFaq, 
                     PublicationRequest, 
                     CartItem,
                     EnrolledCourse
                    )


admin.site.register(Section)
admin.site.register(Course)
admin.site.register(Chapter)



admin.site.register(Lecture)
admin.site.register(LectureStatus)
admin.site.register(CourseBenefit)
admin.site.register(CourseFaq)
admin.site.register(CourseReview)
admin.site.register(PublicationRequest)
admin.site.register(CartItem)
admin.site.register(EnrolledCourse)