from django.shortcuts import render

from django.contrib.admin.views.decorators import staff_member_required
from store.models import Order

from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import StatoOrdineForm
from django.shortcuts import get_object_or_404, redirect


@staff_member_required
def lista_ordini(request):
    search_query = request.GET.get('q', '')
    queryset = Order.objects.all()
    if search_query:
        queryset = queryset.filter(Q(transaction_id__icontains=search_query) | Q(customer__name__icontains=search_query))
    paginator = Paginator(queryset.order_by('-date_ordered'), 10)  # 10 ordini per pagina
    page = request.GET.get('page')
    ordini = paginator.get_page(page)
    return render(request, 'orders/lista_ordini.html', {'ordini': ordini, 'search_query': search_query})



@staff_member_required
def dashboard(request):
    today = timezone.now().date()
    totale = Order.objects.count()
    completati = Order.objects.filter(complete=True).count()
    recenti = Order.objects.order_by('-date_ordered')[:5]
    context = {
        'totale': totale,
        'completati': completati,
        'recenti': recenti,
    }
    return render(request, 'orders/dashboard.html', context)

@staff_member_required
def dettaglio_ordine(request, ordine_id):
    ordine = get_object_or_404(Order, id=ordine_id)
    return render(request, 'orders/dettaglio_ordine.html', {'ordine': ordine})

@staff_member_required
def cambia_stato_ordine(request, ordine_id):
    ordine = get_object_or_404(Order, id=ordine_id)
    if request.method == 'POST':
        form = StatoOrdineForm(request.POST, instance=ordine)
        if form.is_valid():
            form.save()
            return redirect('orders:dettaglio_ordine', ordine_id=ordine.id)
    else:
        form = StatoOrdineForm(instance=ordine)
    return render(request, 'orders/cambia_stato.html', {'form': form, 'ordine': ordine})

class OrdineDelete(DeleteView):
    model = Order
    template_name = 'orders/ordine_confirm_delete.html'
    success_url = reverse_lazy('orders:lista_ordini')



