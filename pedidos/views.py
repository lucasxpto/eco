from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from carrinho.carrinho import Carrinho
from pedidos.forms import PedidoModelForm
from .models import ItemPedido


class PedidoCreateView(CreateView):
    form_class = PedidoModelForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        car = Carrinho(request=self.request)
        pedido = form.save()
        for item in car:
            ItemPedido.objects.create(pedido=pedido,
                                      produto=item['produto'],
                                      preco=item['preco'],
                                      quantidade=item['quantidade'])
        car.limpar()
        return super().form_valid(form)

