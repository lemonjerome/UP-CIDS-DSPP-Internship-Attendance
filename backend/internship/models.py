from django.db import models
from django.contrib.auth.hashers import make_password

class Intern(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('dropped', 'Dropped'),
    ]

    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128)  # Use Django's hashing for security
    full_name = models.CharField(max_length=255)
    start_date = models.DateField()
    time_to_render = models.DurationField()  # Represents the total time to render (e.g., internship duration)
    time_rendered = models.DurationField(default="0:00:00")  # Tracks time already rendered
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')  # New status field

    @property
    def is_authenticated(self):
        # This property is required for Django's authentication system
        return True

    def save(self, *args, **kwargs):
        # Ensure the password is hashed before saving
        if not self.password.startswith('pbkdf2_'):  # Avoid re-hashing an already hashed password
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('validated', 'Validated'),
        ('flagged', 'Flagged'),
        ('sent', 'Sent'),
    ]

    intern = models.ForeignKey(Intern, on_delete=models.CASCADE, related_name="attendance", null=True)  # Connect to Intern table
    type = models.CharField(max_length=255, default="f2f")
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(null=True, blank=True)  # Allow null if the intern hasn't clocked out yet
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')  # New status field
    remarks = models.CharField(max_length=255, blank=True, null=True)  # Optional remarks field


    def __str__(self):
        return f"Attendance for {self.intern.full_name} on {self.time_in.date()}"

class Task(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name="tasks", null=True)  # Many-to-one relationship with Task
    description = models.TextField()
    remarks = models.CharField(max_length=255, blank=True, null=True)  # Optional remarks field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description[:50]  # Return the first 50 characters of the task description

class Image(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="images", null=True)  # Many-to-one relationship with Task
    file = models.ImageField(upload_to='uploads/images/')  # Path where images will be stored
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp of upload

    def __str__(self):
        return self.file.name

