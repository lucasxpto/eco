from django.urls import path
from .views import PedidoCreateView, ResumoPedidoTemplateView

urlpatterns = [
    path('add/', PedidoCreateView.as_view(), name='addpedido'),
    path('resumo/', ResumoPedidoTemplateView.as_view(), name='resumopedido')
]