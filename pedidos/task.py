from celery import shared_task
from .models import Pedido
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@shared_task
def send_email_confirmacao_pedido_task(pedido_id: int) -> None:
    pedido = Pedido.objects.get(id=pedido_id)
    subject = 'Confirmação de pedido'
    from_email = 'pedido@loja.com'
    to = [pedido.email]
    text_content = render_to_string('email_confirmacao_pedido.txt', {'pedido': pedido})
    html_content = render_to_string('email_confirmacao_pedido.html', {'pedido': pedido})

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, 'text/html')
    email.send()