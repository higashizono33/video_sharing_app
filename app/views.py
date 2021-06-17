from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, TemplateView, CreateView
from .models import Video, Resident, Community
from django.urls import reverse_lazy
from .forms import ResidentCreateForm, CommunityCreateForm, VideoCreateForm

class IndexView(TemplateView):
    template_name = 'index.html'

class SelectCommunityView(TemplateView):
    template_name = 'select_community.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['communities'] = Community.objects.filter(owner=self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        community_id = request.POST['community']
        request.session['community_id'] = community_id
        return redirect('home', community_id)

class HomeView(ListView):
    model = Video
    template_name = 'home.html'
    context_object_name = 'videos'
    paginate_by = 8

    def get_queryset(self):
        queryset = super(HomeView, self).get_queryset()
        community = get_object_or_404(Community, pk=self.kwargs['community_id'])
        queryset = Video.objects.filter(community=community)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VideoCreateForm()
        return context

    def post(self, request, *args, **kwargs):
        form = VideoCreateForm(self.request.POST)
        community = get_object_or_404(Community, pk=kwargs['community_id'])
        if form.is_valid():
            new_video = form.save(commit=False)
            new_video.community = community
            form.save()
            return redirect('home', kwargs['community_id'])
        else:
            context = {
                'form': form,
                'videos': Video.objects.filter(community=community),
            }
            return render(request, 'home.html', context)

class CommunityCreateView(CreateView):
    model = Community
    fields = ['name', 'description', 'password']
    template_name = 'community.html'
    success_url = reverse_lazy('create_resident')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

class ResidentCreateView(CreateView):
    model = Resident
    form_class = ResidentCreateForm
    template_name = 'resident.html'
    # success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(ResidentCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs 
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        community = get_object_or_404(Community, pk=self.request.POST['community'])
        form.instance.community = community
        form.save()
        self.request.session['community_id'] = community.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home', kwargs = {'community_id': self.request.POST['community']})

class AddView(CreateView):
    model = Resident
    form_class = ResidentCreateForm
    template_name = 'add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['community_form'] = CommunityCreateForm()
        return context

    def get_form_kwargs(self):
        kwargs = super(AddView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs 
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        community = get_object_or_404(Community, pk=self.request.POST['community'])
        form.instance.community = community
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('add')

def add_community(request):
    if request.method == 'POST':
        community_form = CommunityCreateForm(request.POST)
        if community_form.is_valid():
            community_form.instance.owner = request.user
            community_form.save()
            return redirect('add')
        else:
            form = ResidentCreateForm(user=request.user)
            context = {
                'community_form': community_form,
                'form': form,
            }
        return render(request, 'add.html', context)