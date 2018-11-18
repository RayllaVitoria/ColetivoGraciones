from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .forms import PostForm, PostUpdateForm
from .models import Post
from django.db.models import Q
from django.db import IntegrityError, transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required


class IndexView(TemplateView):
    template_name = 'blog/index.html'


class Post_list(ListView):	
	#posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	model = Post
	template_name = 'blog/post_list.html'
	http_method_names = ['get']	
	context_object_name = 'object_list'

	def get_queryset(self):
		self.queryset = super(Post_list, self).get_queryset()		
		return self.queryset


class Post_detail(DetailView):
	model = Post

	def post_detail_view(request, primary_key):
		post = get_object_or_404(Post, pk=primary_key)
		return render(request, 'blog/post_detail.html', context={'post': post})

class Post_create(CreateView):
	template_name = 'blog/post_add.html'
	models = Post
	form_class = PostForm

class Post_update(UpdateView):
	models = Post
	template_name = 'blog/post_add.html'
	form_class = PostUpdateForm

	def get_queryset(self):
		queryset = Post.objects.all()
		return queryset

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.form_class(instance=self.object)
		return self.render_to_response(self.get_context_data(form=form,))

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()

        # Deletar a capa antigo caso o campo upload files esteja preenchido
		if self.object.capa and self.request.FILES.get('capa', False):
			self.object.capa.delete()

		form = self.form_class(self.request.POST, self.request.FILES, instance=self.object)


		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

		def form_valid(self, form):
			try:
				with transaction.atomic():
					form.save()
					# And notify our users that it worked
					messages.success(self.request, 'Administrador atualizado com sucesso.')
			except IntegrityError: #If the transaction failed
				messages.error(self.request, 'Ocorreu um erro ao atualizar o cadastro do(a) Administrador.')

			return HttpResponseRedirect(self.get_success_url())

		def form_invalid(self, form):
			return self.render_to_response(
			self.get_context_data(
				form=form,
			)
		)

		def get_success_url(self):
			return reverse('blog:post_list')


@login_required
def Post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return render(request, 'blog:index')