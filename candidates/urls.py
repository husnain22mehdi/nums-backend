from django.urls import path

from candidates import views

urlpatterns = [
    path("health", views.health, name="health"),
    path("users", views.candidate_list, name="candidate-list"),
    path(
        "users/<str:roll_number>/exists",
        views.check_roll_number,
        name="check-roll-number",
    ),
    path(
        "users/<str:roll_number>/details",
        views.user_details,
        name="user-details",
    ),
]
