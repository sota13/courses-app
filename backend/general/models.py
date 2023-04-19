from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    reviewer = models.ForeignKey(User,related_name='reviews', on_delete=models.SET_NULL, null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment)
