from django.urls import path
from . import views

app_name = 'pagamento'

urlpatterns = [
    path('processar/', views.ProcessarPagamento.as_view(), name='processar'),
    path('realizado/', views.PagamentoRealizadoView.as_view(), name='realizado'),
    path('cancelado/', views.PagamentoCanceladoView.as_view(), name='cancelado'),
]