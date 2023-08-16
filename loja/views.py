from django.views.generic import ListView, DetailView

from loja.models import Categoria, Produto


class ProdutoListView(ListView):
    template_name = 'loja/produtos/listar.html'
    model = Produto
    queryset = Produto.disponiveis.all()
    context_object_name = 'produtos'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        categoria = None
        categorias = Categoria.objects.all()
        if self.kwargs and self.kwargs['categ_slug']:
            slug = self.kwargs['categ_slug']
            categoria = Categoria.objects.filter(slug=slug)
            self.queryset = self.queryset.filter(categoria=categoria)
        contexto['categoria'] = categoria
        contexto['categorias'] = categorias
        print(contexto)
        return contexto


class ProdutoDetailView(DetailView):
    template_name = 'loja/produtos/detalhe.html'
    model = Produto