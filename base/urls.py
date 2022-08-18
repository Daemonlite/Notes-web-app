from django.urls import path
from .views import  CustomLoginView, NotesCreate,DeleteView, NotesDetail, NotesList, NotesReorder, NotesUpdate, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),


    path('', NotesList.as_view(), name='notes'),
    path('note/<int:pk>/', NotesDetail.as_view(), name='note'),
    path('note-create/', NotesCreate.as_view(), name='note-create'),
    path('note-update/<int:pk>/', NotesUpdate.as_view(), name='note-update'),
    path('note-delete/<int:pk>/', DeleteView.as_view(), name='note-delete'),
    path('note-reorder/',NotesReorder.as_view(), name='note-reorder'),

]