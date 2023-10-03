from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from carrinho.carrinho import Carrinho
from pedidos.forms import PedidoModelForm
from .models import ItemPedido, Pedido


class PedidoCreateView(CreateView):
    form_class = PedidoModelForm
    success_url = reverse_lazy('resumopedido')
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
        self.request.session['idpedido'] = pedido.id
        self.email_confirmacao_pedido(pedido)
        return redirect('resumopedido', idpedido=pedido.id)

    def email_confirmacao_pedido(self, pedido: Pedido) -> None:
        subject = 'Confirmação de pedido'
        from_email = 'pedido@loja.com'
        to = [pedido.email]
        text_content = render_to_string('email_confirmacao_pedido.txt', {'pedido': pedido})
        html_content = render_to_string('email_confirmacao_pedido.html', {'pedido': pedido})

        email = EmailMultiAlternatives(subject, text_content, from_email, to)
        email.attach_alternative(html_content, 'text/html')
        email.send()
        
class ResumoPedidoTemplateView(TemplateView):
    template_name = 'resumopedido.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pedido'] = Pedido.objects.get(id=self.kwargs['idpedido'])
        return ctx

