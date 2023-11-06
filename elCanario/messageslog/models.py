from django.db import models
# Create your models here.
class MessageLog(models.Model):
    '''Message logging. It will show when a write, delete or update action was performed or attempted on any other model in the system.'''
    info = models.TextField(max_length=500, unique=False, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True,editable=False)
    
    class Meta:

        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-date']

    def __str__(self):
        return f"Message: {self.info}, Date: {self.date}"

