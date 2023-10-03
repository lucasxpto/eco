from django.shortcuts import render, reverse
from django.urls import reverse_lazy

from ecommerce import settings
from pagamentos.forms import CheckoutForm
from pedidos.models import Pedido
from django.views.generic import TemplateView, FormView
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import braintree


class ProcessarPagamento(FormView):
    template_name = 'pagamento/processar.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('pagamento:realizado')

    def dispatch(self, request, *args, **kwargs):
        braintree_env = braintree.Environment.Sandbox
        braintree.Configuration.configure(
            braintree_env,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY
        )
        self.braintree_client_token = braintree.ClientToken.generate({})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['braintree_client_token'] = self.braintree_client_token
        return ctx

    def form_valid(self, form):
        idpedido = self.request.session.get('idpedido')
        pedido = Pedido.objects.get(id=idpedido)
        custo_total = pedido.get_total()
        result = braintree.Transaction.sale({
            'amount': custo_total,
            'payment_method_nonce': form.cleaned_data['payment_method_nonce'],
            'options': {
                'submit_for_settlement': True,
            },
        })
        if result.is_success:
            context = self.get_context_data()
            context['form'] = self.get_form(self.get_form_class())
            context['braintree_error'] = 'Pagamento não processado. Favor verificar os dados.'
            self.email_pagamento_aprovado(pedido)
        return super().form_valid(form)

    def email_pagamento_aprovado(self, pedido: Pedido) -> None:
        subject = 'Pagamento aprovado'
        from_email = 'pagamento@loja.com'
        to = [pedido.email]
        text_content = render_to_string('email_pagamento_aprovado.txt', {'pedido': pedido})
        html_content = render_to_string('email_pagamento_aprovado.html', {'pedido': pedido})

        email = EmailMultiAlternatives(subject, text_content, from_email, to)
        email.attach_alternative(html_content, 'text/html')
        email.send()

class PagamentoRealizadoView(TemplateView):
    template_name = 'pagamento/realizado.html'


class PagamentoCanceladoView(TemplateView):
    template_name = 'pagamento/cancelado.html'
