from django.http import JsonResponse
from django.shortcuts import render
from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Habit, HabitTimerSession
from .forms import HabitForm

@login_required
def habit_timer_start(request, habit_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    habit = get_object_or_404(Habit, id=habit_id, user=request.user)

    if not habit.use_timer:
        return JsonResponse(
            {"error": "This habit does not use a timer"},
            status=400
        )

    active_session = HabitTimerSession.objects.filter(
        habit=habit,
        user=request.user,
        stopped_at__isnull=True
    ).first()

    if active_session:
        session = active_session
    else:
        session = HabitTimerSession.objects.create(
            habit=habit,
            user=request.user
        )

    return JsonResponse({
        "session_id": session.id,
        "started_at": session.started_at.isoformat(),
        "required_seconds": habit.required_minutes * 60,
    })
@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)

    return render(request, "habits/habit_list.html", {
        "habits": habits
    })

@login_required
def habit_create(request):
    if request.method == "POST":
        form = HabitForm(request.POST)

        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()

            return redirect('habit_list')
    else:
        form = HabitForm()

    return render(request, 'habits/habit_create.html', {'form': form})

@login_required
def habit_done(request, habit_id):
    habit = get_object_or_404(
        Habit,
        id=habit_id,
        user=request.user
    )

    if request.method != "POST":
        return redirect("habit_list")

    if habit.last_done_date == timezone.localdate():
        return redirect("habit_list")

    if habit.use_timer:
        session = HabitTimerSession.objects.filter(
            habit=habit,
            user=request.user,
            stopped_at__isnull=True
        ).order_by("-started_at").first()

        if not session:
            messages.error(
                request,
                "Start the timer first."
            )
            return redirect("habit_list")

        elapsed_seconds = (
            timezone.now() - session.started_at
        ).total_seconds()

        required_seconds = habit.required_minutes * 60

        if elapsed_seconds < required_seconds:
            messages.error(
                request,
                "Required timer duration has not passed yet."
            )
            return redirect("habit_list")

        session.stopped_at = timezone.now()
        session.completed = True
        session.save()

    habit.streak += 1
    habit.last_done_date = date.today()
    habit.save()

    return redirect("habit_list")

@login_required
def habit_delete(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)

    if request.method == "POST":
        habit.delete()
        return redirect('habit_list')

    return render(request, 'habits/habit_confirm_delete.html', {'habit': habit})
