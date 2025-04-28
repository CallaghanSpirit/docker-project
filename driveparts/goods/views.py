from django.shortcuts import render,HttpResponse,get_object_or_404, redirect
from goods.models import Goods, Category, Tags, UploadFiles
from goods.forms import AddPostForm, UploadFileForm, ContactForm
from pathlib import Path
from django.core.exceptions import ValidationError
from django.views import View
from django.views.generic import  ListView, DetailView, FormView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .utils import DataMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache

# Create your views here.
# def index(request):
#     goods = Goods.manager.all()
#     data = {
#         'title':'Главная страница',
#         'goods':goods
        
#         }
#     return render(request,template_name='goods/index.html',context=data)

class GoodsHome(DataMixin,ListView):
    # model = Goods
    template_name = "goods/index.html"
    context_object_name = 'goods'
    extra_context = {
        'title':'Главная страница',
        }
    
    def get_queryset(self):
        g_lst = cache.get("goods_posts")
        if not g_lst:
            g_lst = Goods.manager.all()
            cache.set("goods_posts", g_lst , 60)
        return g_lst
    
    # Работает при непосредственном вызове Get запроса
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Пидор'
   

class GoodsCategory(DataMixin, ListView):
    # model = Category
    template_name = "goods/index.html"
    context_object_name = "goods"
    allow_empty = True
    
    def get_queryset(self):
        return Goods.manager.filter(cats__slug=self.kwargs['cat_slug'])

@permission_required(perm='goods.view_goods', raise_exception=True)
def cardpage(request,gd_slug):
    goods = get_object_or_404(Goods,slug=gd_slug)
    data = {"goods":goods,}
    return render(request,template_name='goods/cardpage.html',context=data)

class CardPage(DetailView):
    # model = Goods
    template_name = 'goods/cardpage.html'
    slug_url_kwarg = 'gd_slug'
    context_object_name = 'goods'

    def get_object(self, queryset = Goods):
        return get_object_or_404(queryset.manager, slug = self.kwargs[self.slug_url_kwarg])

class GoodsTags(DataMixin, ListView):
    template_name = 'goods/index.html'
    context_object_name = 'goods'
    def get_queryset(self):
        return Goods.manager.filter(tags__slug=self.kwargs['tag_slug'])


class AddProd(PermissionRequiredMixin ,LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    login_url = ''
    # model = Goods
    # fields = '__all__'
    template_name = 'goods/add_prod.html'
    # success_url = reverse_lazy('home')
    permission_required = 'goods.add_goods' # <приложение>.<действие>_<таблица>

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

class DeletePage(DeleteView):
    model = Goods
    fields = '__all__'
    template_name = 'goods/add_prod.html'
    success_url = reverse_lazy('home')

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)

# class AddProd(View):
#     def get(self, request):
#         form = AddPostForm()
#         data = {
#         'title':'Добавление товара',
#         'form':form   

#             }
#         return render(request, 'goods/add_prod.html', context=data)

#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         data = {
#         'title':'Добавление товара',
#         'form':form   

#             }
#         return render(request, 'goods/add_prod.html', context=data)

def handle_uploaded_file(f):
    with open(f'uploads/{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required(login_url='')
def about(request):
    contact_list = Goods.manager.all()
    paginator = Paginator(contact_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        'title': 'О сайте',
        'page_obj': page_obj,


    }
    return render(request, 'goods/about.html', context=data)

class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'goods/contact.html'
    success_url = reverse_lazy('home')
    title_page = 'Обратная связь'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)