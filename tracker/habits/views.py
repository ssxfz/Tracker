from django.shortcuts import render
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Habit
from .forms import HabitForm

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
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)

    today = date.today()

    if habit.last_done_date != today:
        habit.streak += 1
        habit.last_done_date = today
        habit.save()
    return redirect('habit_list')

@login_required
def habit_delete(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)

    if request.method == "POST":
        habit.delete()
        return redirect('habit_list')

    return render(request, 'habits/habit_confirm_delete.html', {'habit': habit})
