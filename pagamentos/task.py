from celery import shared_task
from pedidos.models import Pedido
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@shared_task
def send_email_pagamento_confirmado_task(pedido_id: int) -> None:
    pedido = Pedido.objects.get(id=pedido_id)
    subject = 'agamento aprovado'
    from_email = 'pedido@loja.com'
    to = [pedido.email]
    text_content = render_to_string('email_pagamento_aprovado.txt', {'pedido': pedido})
    html_content = render_to_string('email_pagamento_aprovado.html', {'pedido': pedido})

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, 'text/html')
    email.send()