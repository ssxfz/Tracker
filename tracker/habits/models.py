from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    use_timer = models.BooleanField(default=False)
    required_minutes = models.PositiveIntegerField(
        default=10
    )
    streak = models.IntegerField(default=0)
    last_done_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_done_today(self):
        return self.last_done_date == timezone.localdate()

    def __str__(self):
        return self.title

class HabitTimerSession(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="timer_sessions"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    started_at = models.DateTimeField(auto_now_add=True)
    stopped_at = models.DateTimeField(null=True, blank=True)

    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.habit.title} - {self.started_at}"