from django.urls import path
from .views import (CoachRegisterView,
                    StudentRegisterView,
                    LoginView,
                    StudentListView,
                    StudentDetailView,
                    CreateGroupView,
                    AddStudentToGroupView,
                    SeeStudentsListInGroupView,
                    DeleteStudentFromGroupView,
                    UpdateBeltStatusView,
                    AddRatingPointsView,
                    StudentProfileView,
                    StudentDeleteView,
                    SeeGroupView,
                    GroupDetailView
                    )

urlpatterns = [
    path('student/profile/', StudentProfileView.as_view(), name='my-profile'),
    path('register/coach', CoachRegisterView.as_view(), name='coach-register'),
    path('register/student/', StudentRegisterView.as_view(), name='student-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('student_list/', StudentListView.as_view(), name='student-list'),
    path('<int:id>/', StudentDetailView.as_view(), name='student-detail'),
    path('coach/create_group/', CreateGroupView.as_view(), name='create-group'),

    path('groups/', SeeGroupView.as_view(), name='see-groups'),
    path('groups/<int:group_id>', GroupDetailView.as_view(), name='see-group-detail'),
    path('groups/<int:group_id>/add-student/<int:student_id>/', AddStudentToGroupView.as_view(), name='add-to-group'),
    path('groups/<int:group_id>/delete_student/<int:student_id>/', DeleteStudentFromGroupView.as_view(), name='delete-from-group'),
    path('groups/<int:group_id>/students', SeeStudentsListInGroupView.as_view(), name='group-students-list'),


    path('<int:student_id>/update_belt_status/', UpdateBeltStatusView.as_view(), name='update-belt-status'),
    path('<int:student_id>/add_rating_points/', AddRatingPointsView.as_view(), name='add-rating-points'),
    path('<int:id>/delete/', StudentDeleteView.as_view(), name='student-delete')

]

