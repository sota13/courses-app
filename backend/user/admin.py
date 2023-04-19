from django.contrib import admin

from user.models import UserProfile



class ProfileAdmin(admin.ModelAdmin):
    # fields = [
    #     'user',
    #     'first_name',
    #     'last_name',
    #     'status',
    #     'bio',
    # ]
    list_display = [
        'user',
        'gender',
        'bio',
    ]


# register the Profile model .
admin.site.register(UserProfile, ProfileAdmin)
