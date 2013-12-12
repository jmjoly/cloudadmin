from django.views.generic.list import ListView
from django.utils import timezone

from vms.models import Vm

class VmListView(ListView):

    model = Vm

    def get_context_data(self, **kwargs):
        context = super(VmListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
