from django.contrib.auth import login
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, TemplateView, CreateView
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from .models import Comment, Video, Resident, Community, Post
from django.urls import reverse_lazy
from .forms import ResidentCreateForm, CommunityCreateForm, VideoCreateForm, ResidentLoginForm, GroupCreateForm
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import check_password


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
        community = get_object_or_404(Community, pk=self.kwargs['community_id'])
        context['community'] = community
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
            community = get_object_or_404(Community, pk=self.kwargs['community_id'])
            context = {
                'form': form,
                'videos': Video.objects.filter(community=community),
                'community': community
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
        context['group_form'] = GroupCreateForm(user=self.request.user)
        context['community'] = get_object_or_404(Community, pk=self.request.session['community_id'])
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
            group_form = GroupCreateForm(user=request.user)
            context = {
                'community_form': community_form,
                'group_form': group_form,
                'form': form,
            }
        return render(request, 'add.html', context)

def add_group(request):
    if request.method == 'POST':
        group_form = GroupCreateForm(request.POST, user=request.user)
        if group_form.is_valid():
            group_form.save()
            return redirect('add')
        else:
            form = ResidentCreateForm(user=request.user)
            community_form = CommunityCreateForm()
            context = {
                'community_form': community_form,
                'group_form': group_form,
                'form': form,
            }
        return render(request, 'add.html', context)

class VideoDetailView(DetailView):
    model = Video
    template_name = 'video.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['community'] = get_object_or_404(Community, pk=self.request.session['community_id'])
        video = get_object_or_404(Video, pk=self.kwargs['pk'])
        group = self.object.group
        context['videos'] = Video.objects.filter(group=group).order_by('-created_at')
        context['posts'] = Post.objects.filter(posted_to=video).order_by('-created_at')
        context['comments'] = Comment.objects.all().order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        video = get_object_or_404(Video, pk=kwargs['pk'])
        if 'resident_id' not in request.session:
            new = Post.objects.create(
                user_posted = request.user,
                posted_to = video,
                post = request.POST['post']
            )
        else:
            resident = get_object_or_404(Resident, pk=request.session['resident_id'])
            new = Post.objects.create(
                resident_posted = resident,
                posted_to = video,
                post = request.POST['post']
            )
        return redirect('video', pk=kwargs['pk'])

def reply_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        if 'resident_id' not in request.session:
            new = Comment.objects.create(
                user_commented = request.user,
                commented_to = post,
                comment = request.POST['comment']
            )
        else:
            resident = get_object_or_404(Resident, pk=request.session['resident_id'])
            new = Comment.objects.create(
                resident_commented = resident,
                commented_to = post,
                comment = request.POST['comment']
            )
    return redirect('video', pk=request.POST['video_id'])
    
class ResidentLoginView(FormView):
    template_name = 'registration/resident_login.html'
    form_class = ResidentLoginForm
    # success_url = '/index/'
    
    def form_valid(self, form):
        community = get_object_or_404(Community, pk=self.kwargs['community_id'])
        if check_password(self.request.POST['password'], community.password):
            residents = Resident.objects.filter(community=community)
            for resident in residents:
                if resident.name == self.request.POST['name']:
                    self.request.session.flush()
                    self.request.session['resident_id'] = resident.id
                    self.request.session['community_id'] = community.id
                    return redirect('home', community.id)
        else:
            return redirect('resident_login', self.kwargs['community_id'])

def resident_logout(request):
    id = request.session['community_id']
    request.session.flush()
    return redirect('resident_login', id)

class ManageResidentView(ListView):
    template_name = 'manage.html'
    model = Resident
    context_object_name = 'residents'

    def get_queryset(self):
        queryset = super(ManageResidentView, self).get_queryset()
        community = get_object_or_404(Community, pk=self.request.session['community_id'])
        queryset = Resident.objects.filter(community=community)
        return queryset

def delete_resident(request, resident_id):
    resident = get_object_or_404(Resident, pk=resident_id)
    resident.delete()
    return redirect('manage_resident')