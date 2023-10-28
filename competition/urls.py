from django.urls import path
from .views import (SeeCompetitionsListView,
                    CreateCompetitionView,
                    AddStudentsToCompetitionView,
                    CompetitionDetailView,
                    SeeStudentInCompetitions)

urlpatterns = [
    path("create_competition/", CreateCompetitionView.as_view(), name="create-competition"),
    path("competition_list/", SeeCompetitionsListView.as_view(), name="competition-list"),
    path("<int:competition_id>/student/<int:student_id>/add_student_to_competition/",  AddStudentsToCompetitionView.as_view(), name="add-students-to-competition"),
    path("<int:id>/", CompetitionDetailView.as_view(), name="competition-detail"),
    path("<int:competition_id>/see_students/", SeeStudentInCompetitions.as_view(), name="sostav" )
]