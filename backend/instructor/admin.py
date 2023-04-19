from django.contrib import admin
from .models import (Instructor, 
InstructorRequest, 
InstructorReview, 
InstructorEducation,
InstructorSkill,
InstructorContactInfo,
InstructorSocialMedia,
SocialMediaItem,
ContactItem,
ListingRequest)




admin.site.register(Instructor)
admin.site.register(InstructorRequest)
admin.site.register(InstructorReview)
admin.site.register(InstructorEducation)
admin.site.register(InstructorSkill)
admin.site.register(InstructorContactInfo)
admin.site.register(InstructorSocialMedia)
admin.site.register(SocialMediaItem)
admin.site.register(ContactItem)
admin.site.register(ListingRequest)
