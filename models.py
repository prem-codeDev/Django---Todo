from django.db import models

# Create your models here.
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),  
]

class Task(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')  
    progress = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name

class TaskHistory(models.Model):
    name = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)
    status = models.CharField(max_length=20)