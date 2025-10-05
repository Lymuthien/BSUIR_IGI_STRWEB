from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Client, Employee, User


class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class AdminClientListView(LoginRequiredMixin, SuperUserRequiredMixin, ListView):
    model = Client
    template_name = 'admin_clients.html'
    context_object_name = 'clients'
    paginate_by = 20

    def get_queryset(self):
        return Client.objects.select_related('user').order_by('-user__date_joined')


class AdminEmployeeListView(LoginRequiredMixin, SuperUserRequiredMixin, ListView):
    model = Employee
    template_name = 'admin_employees.html'
    context_object_name = 'employees'
    paginate_by = 20

    def get_queryset(self):
        return Employee.objects.select_related('user').order_by('-hire_date')


class AdminClientUpdateView(LoginRequiredMixin, SuperUserRequiredMixin, UpdateView):
    model = User
    template_name = 'admin_client_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'is_active']
    success_url = reverse_lazy('admin_clients')

    def form_valid(self, form):
        messages.success(self.request, 'Данные клиента успешно обновлены')
        return super().form_valid(form)


class AdminEmployeeUpdateView(LoginRequiredMixin, SuperUserRequiredMixin, UpdateView):
    model = User
    template_name = 'admin_employee_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'is_active']
    success_url = reverse_lazy('admin_employees')

    def form_valid(self, form):
        messages.success(self.request, 'Данные сотрудника успешно обновлены')
        return super().form_valid(form)


class AdminEmployeeCreateView(LoginRequiredMixin, SuperUserRequiredMixin, CreateView):
    model = User
    template_name = 'admin_employee_form.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'birth_date']
    success_url = reverse_lazy('admin_employees')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = 'employee'
        user.set_password('temp_password')  # Временный пароль
        user.save()

        # Создаем сотрудника
        Employee.objects.create(
            user=user,
            hire_date=timezone.now().date()
        )

        messages.success(self.request, f'Сотрудник {user.username} успешно создан')
        return redirect(self.success_url)


class AdminEmployeeDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):
    model = User
    template_name = 'admin_confirm_delete.html'
    success_url = reverse_lazy('admin_employees')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        messages.success(request, f'Пользователь {user.username} удален')
        return super().delete(request, *args, **kwargs)


def toggle_client_status(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'Недостаточно прав')
        return redirect('admin_clients')

    client = get_object_or_404(Client, pk=pk)
    client.user.is_active = not client.user.is_active
    client.user.save()

    status = "разблокирован" if client.user.is_active else "заблокирован"
    messages.success(request, f'Клиент {client.user.username} {status}')

    return redirect('admin_clients')