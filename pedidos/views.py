'''
Lucas Pedreira Vital
'''
from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .task import send_email_confirmacao_pedido_task

from carrinho.carrinho import Carrinho
from pedidos.forms import PedidoModelForm
from .models import ItemPedido, Pedido


class PedidoCreateView(CreateView):
    form_class = PedidoModelForm
    template_name = 'formpedido.html'

    def form_valid(self, form):
        car = Carrinho(request=self.request)
        pedido = form.save()
        for item in car:
            ItemPedido.objects.create(pedido=pedido,
                                      produto=item['produto'],
                                      preco=item['preco'],
                                      quantidade=item['quantidade'])
        car.limpar()
        self.request.session['idPedido'] = pedido.id
        send_email_confirmacao_pedido_task.delay(pedido.id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('resumopedido', args=[self.object.id])

class ResumoPedidoTemplateView(TemplateView):
    template_name = 'resumopedido.html'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        idpedido = self.request.session.get('idPedido')
        if idpedido:
            ctx['pedido'] = Pedido.objects.get(id=idpedido)
        return ctx
