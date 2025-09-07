from django.db import models
from django.contrib.auth.models import AbstractUser

class Permission(models.Model):
    designation_level = models.IntegerField(unique=True, help_text="The level this permission rule applies to.")

    can_assign = models.BooleanField(default=False, help_text="Can users at this level assign tasks to lower levels?")

   
    can_assign_to_same_level = models.BooleanField(
        default=False,
        help_text="Can users at this level assign tasks to users at the SAME level?"
    )

    def __str__(self):
        return f"Permissions for Level {self.designation_level}"

class User(AbstractUser):
    designation_level = models.IntegerField(default=1, help_text="User's role level, links to a Permission entry.")

    def __str__(self):
        return self.username

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True, blank=True)

    class Status(models.TextChoices):
        TODO = 'TODO', 'To Do'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        DONE = 'DONE', 'Done'

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

