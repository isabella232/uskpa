from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import permission_required
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from .forms import CertificateRegisterForm
from .models import Certificate
from .filters import CertificateFilter
from .utils import _filterable_params
from django.contrib.auth import get_user_model

User = get_user_model()


@permission_required('accounts.can_get_licensee_contacts', raise_exception=True)
def licensee_contacts(request):
    """Return users associated with the provided licensee"""
    if request.method == 'GET':
        licensee_id = request.GET.get('licensee')
        contacts = User.objects.filter(profile__licensees=licensee_id) if licensee_id else []
        if contacts:
            contacts_json = [{'id': user.id, 'name': user.profile.get_user_display_name()} for user in contacts]
        else:
            contacts_json = []
    else:
        return HttpResponse(status=405)
    return JsonResponse(contacts_json, safe=False)


class CertificateRegisterView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    raise_exception = True

    def test_func(self):
        """only for superusers"""
        if self.request.user.is_superuser:
            return True

    template_name = 'certificate/register.html'
    form_class = CertificateRegisterForm
    success_url = reverse_lazy('cert-register')

    def form_valid(self, form):
        """Generate requested Certificates"""
        cert_kwargs = {'assignor': self.request.user, 'licensee': form.cleaned_data['licensee'],
                       'date_of_sale': form.cleaned_data['date_of_sale']}
        certs = form.get_cert_list()
        if certs:
            Certificate.objects.bulk_create(Certificate(number=i, **cert_kwargs) for i in certs)
        messages.success(self.request, f'Generated {len(certs)} new certificates.')
        return super().form_valid(form)


class CertificateListView(TemplateView):
    template_name = 'certificate/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = CertificateFilter(self.request.GET, queryset=self.request.user.profile.certificates())
        return context


class CertificateJson(LoginRequiredMixin, BaseDatatableView):
    model = Certificate
    columns = ['number', 'status', 'consignee', 'last_modified', 'shipped_value']
    order_columns = columns

    max_display_length = 500

    def get_initial_queryset(self):
        """Limit to certificates visible to user"""
        return self.request.user.profile.certificates()

    def filter_queryset(self, qs):
        # Filter by certificate number
        search = self.request.GET.get('search[value]')
        qs = CertificateFilter(
            _filterable_params(self.request.GET), queryset=qs).qs
        if search:
            qs = qs.filter(number__istartswith=search)
        return qs

    def prepare_results(self, qs):
        """format our dates and Cert number"""
        json_data = []
        for item in qs:
            json_data.append([
                str(item),
                item.get_status_display(),
                item.consignee,
                item.last_modified.strftime("%Y-%m-%d %H:%M:%S"),
                f'${item.shipped_value}' if item.shipped_value else None
            ])
        return json_data
