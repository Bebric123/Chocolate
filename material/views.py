from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, View
from .models import *
from .forms import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Sum
# Create your views here.

ROLES_CAN_CREATE = ['Администратор']
ROLES_CAN_UPDATE = ['Администратор', 'Менеджер']
ROLES_CAN_MANAGE = ['Администратор']


class RoleRequiredMixin:
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, 'Login in system')
            return redirect('login')
        role = request.session.get('role_name', '')
        if role not in self.allowed_roles:
            messages.error(
                request,
                f'You not have permisions. Your role - {role}'
            )
            return redirect('materials_list')
        return super().dispatch(request, *args, **kwargs)

    
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if 'user_id' in request.session:
            return redirect('materials_list')
        return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            # password = form.cleaned_data['password']
            try:
                user = Users.objects.select_related('role').get(login=login,)
                request.session['user_id'] = user.id
                request.session['user_name'] = user.full_name
                request.session['role_name'] = user.role.name_role if user.role else ""
                messages.success(request, f'Hello {user.full_name}')
            except Users.DoesNotExist:
                messages.error(request, "Incorect login or password")
            return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        request.session.flush()
        messages.success(request, 'You logout')
        return redirect('login')


class MaterialsListView(ListView):
    model = Materials
    template_name = 'list_material.html'
    context_object_name = 'materials'

    def dispatch(self, request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request,'Login in system')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Materials.objects.annotate(
            summ = Sum('materialproducts__qty_material_product')
        )


class MaterialCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ROLES_CAN_CREATE
    model = Materials
    form_class = MaterialForm
    template_name = 'create_material.html'
    context_object_name = 'materials'
    success_url = reverse_lazy('materials_list')

    def form_valid(self, form):
        messages.success(self.request, 'Material added')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'Material added error, try again')
        return super().form_invalid(form)

    
class MaterialUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ROLES_CAN_UPDATE
    model = Materials
    form_class = MaterialForm
    template_name = 'update_material.html'
    context_object_name = 'materials'
    success_url = reverse_lazy('materials_list')

    def form_valid(self, form):
        messages.success(self.request, 'Material updated')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'Material updated error, try again')
        return super().form_invalid(form)


class SuppliersListView(ListView):
    model = Materials
    template_name = 'supplier_list.html'
    context_object_name = 'materials'

    def get_queryset(self):
        return MaterialSuppliers.objects.filter(material_id=self.kwargs['pk'])

class UserListView(RoleRequiredMixin, ListView):
    allowed_roles = ROLES_CAN_MANAGE
    model = Users
    template_name = 'list_users.html'
    context_object_name = 'users'

    def get_queryset(self):
        return Users.objects.select_related('role').all()


class UserRoleUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ROLES_CAN_MANAGE
    model = Users
    form_class = UserRoleForm
    template_name = 'user_role_update.html'
    context_object_name = 'user_obj'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Роль пользователя успешно изменена.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при изменении роли.')
        return super().form_invalid(form)


class SupplierUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ROLES_CAN_MANAGE
    model = Suppliers
    form_class = SupplierForm
    template_name = 'supplier_update.html'
    context_object_name = 'supplier_obj'
    success_url = reverse_lazy('materials_list')

    def form_valid(self, form):
        messages.success(self.request, 'Поставщик успешно изменен.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при изменении поствщика.')
        return super().form_invalid(form)


class ProductListView(ListView):
    model = Materials
    template_name = 'product_list.html'
    context_object_name = 'materials'

    def get_queryset(self):
        return MaterialProducts.objects.filter(material_id=self.kwargs['pk'])


def calculate_product(product_type_id:int, material_type_id:int, qty_material: int, param1: float, param2:float) -> int:    
    try:
        if qty_material <= 0 or param1 <= 0 or param2 <= 0:
            return -1

        product_type = ProductType.objects.get(id=product_type_id)
        material_type = MaterialType.objects.get(id=material_type_id)

        if product_type is None or material_type is None:
            return -1

        coeff_product = material_type.coeff_product
        percent_lost = product_type.percent_lost

        qty_product = param1 * param2 * coeff_product
        result = qty_material / qty_product * (1 - percent_lost/100)
        return int(result)
    except Exception as e:
        return -1

    