from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('loja.urls')),
    path('carrinho/', include('carrinho.urls')),
    path('pedido/', include('pedidos.urls')),
    path('pagamento/', include('pagamentos.urls', namespace='pagamento')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
