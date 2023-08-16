from django.urls import path
from loja import views

urlpatterns = [
    path('', views.ProdutoListView.as_view(), name='listarprod'),
    path('<slug:categ_slug>', views.ProdutoListView.as_view(), name='listarprodcateg'),
    path('produto/<pk>/<slug>', views.ProdutoDetailView.as_view(), name='detalheprod'),
]