from django.urls import path
from .views import (
    dashboard, lista_ordini, dettaglio_ordine, cambia_stato_ordine, OrdineDelete
)

app_name = 'orders'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('', lista_ordini, name='lista_ordini'),
    path('<int:ordine_id>/', dettaglio_ordine, name='dettaglio_ordine'),
    path('<int:ordine_id>/cambia-stato/', cambia_stato_ordine, name='cambia_stato_ordine'),
    path('<int:pk>/delete/', OrdineDelete.as_view(), name='ordine_delete'),
]

