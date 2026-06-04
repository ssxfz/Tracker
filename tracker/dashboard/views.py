from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def schedule_page(request):
    lessons = [
        {
            "day": "Субота",
            "date": "06.06.2026",
            "start_column": 2,
            "end_column": 4,
            "title": "2 СБ 10:00",
            "course": "Unity 2D",
            "location": "Kyiv-04-Poznyaki",
            "time": "10:00 - 12:00",
        },
        {
            "day": "Неділя",
            "date": "07.06.2026",
            "start_column": 3,
            "end_column": 5,
            "title": "Django",
            "course": "Python Middle",
            "location": "Online",
            "time": "11:00 - 13:00",
        },
    ]

    return render(request, "dashboard/schedule.html", {
        "lessons": lessons
    })