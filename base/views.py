from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Notes
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from .forms import PositionForm
from django.views import View
from django.db import transaction

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('notes')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('notes')
        return super(RegisterPage, self).get(*args, **kwargs)

class NotesList( LoginRequiredMixin,ListView):
    model = Notes
    context_object_name = 'notes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(user=self.request.user)
        context['count'] = context['notes'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['notes'] = context['notes'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context


class NotesDetail(LoginRequiredMixin,DetailView):
    model = Notes
    context_object_name = 'note'
    template_name = 'base/note.html'


class NotesCreate(LoginRequiredMixin, CreateView):
    model = Notes
    fields = ['title', 'description','body', 'complete']
    template_name = 'base/note_create.html'
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(NotesCreate, self).form_valid(form)

class NotesUpdate(LoginRequiredMixin, UpdateView):
    model = Notes
    fields = ['title', 'description','body', 'complete']
    success_url = reverse_lazy('notes')

class DeleteView (DeleteView):
    model = Notes
    context_object_name = 'note'
    success_url = reverse_lazy('notes')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class NotesReorder(LoginRequiredMixin,View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('notes'))