from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # This gets your CustomUser model

class AdminActivity(models.Model):
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Admin Activities'

    def __str__(self):
        return f"{self.admin_user.email} - {self.action}"