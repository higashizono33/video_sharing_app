from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, TemplateView, CreateView
from django.views.generic.detail import DetailView
from .models import Comment, Video, Resident, Community, Post, VideoGroup
from django.urls import reverse_lazy
from .forms import ResidentCreateForm, CommunityCreateForm, VideoCreateForm, ResidentLoginForm, GroupCreateForm
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.contrib import messages

import re

# convert url to embedded type
yt_link = re.compile(r'(https?://)?(www\.)?((youtu\.be/)|(youtube\.com/watch/?\?v=))([A-Za-z0-9-_]+)', re.I)
yt_embed = "https://www.youtube.com/embed/{0}"

def convert_ytframe(text):
    return yt_link.sub(lambda match: yt_embed.format(match.groups()[5]), text)

class IndexView(TemplateView):
    template_name = 'intro.html'

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
    paginate_by = 4

    def get_queryset(self):
        queryset = super(HomeView, self).get_queryset()
        community = get_object_or_404(Community, pk=self.kwargs['community_id'])
        queryset = Video.objects.filter(community=community).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VideoCreateForm(community_id=self.kwargs['community_id'])
        community = get_object_or_404(Community, pk=self.kwargs['community_id'])
        if 'resident_id' in self.request.session:
            resident = get_object_or_404(Resident, pk=self.request.session['resident_id'])
            context['resident'] = resident
        context['community'] = community
        return context

    def post(self, request, *args, **kwargs):
        form = VideoCreateForm(self.request.POST, community_id=self.kwargs['community_id'])
        community = get_object_or_404(Community, pk=kwargs['community_id'])
        if form.is_valid():
            new_video = form.save(commit=False)
            new_video.url = convert_ytframe(self.request.POST['url'])
            new_video.community = community
            form.save()
            return JsonResponse({'success': True})
        else:
            ctx = {}
            ctx.update(csrf(request))
            form_html = render_crispy_form(form, context=ctx)
            return JsonResponse({'success': False, 'form_html': form_html})

def delete_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    video.delete()
    return redirect('home', request.session['community_id'])

class CommunityCreateView(CreateView):
    model = Community
    form_class = CommunityCreateForm
    template_name = 'community.html'
    success_url = reverse_lazy('create_resident')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        new_community = form.save()
        print(new_community.id)
        self.request.session['community_id'] = new_community.id
        return super().form_valid(form)

class ResidentCreateView(CreateView):
    model = Resident
    form_class = ResidentCreateForm
    template_name = 'resident.html'
    success_url = reverse_lazy('create_resident')

    def get_form_kwargs(self):
        kwargs = super(ResidentCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs 

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        community = get_object_or_404(Community, pk=self.request.session['community_id'])
        obj.community = community
        obj.save()
        messages.success(self.request, f'{obj.name} was added')

        return super().form_valid(form)

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
        name = self.request.POST['name']
        messages.success(self.request, f'{name} was added')
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
            community = get_object_or_404(Community, pk=request.session['community_id'])
            context = {
                'community_form': community_form,
                'group_form': group_form,
                'form': form,
                'community': community,
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
            community = get_object_or_404(Community, pk=request.session['community_id'])
            context = {
                'community_form': community_form,
                'group_form': group_form,
                'form': form,
                'community': community,
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
        videos = Video.objects.filter(group=group).order_by('-created_at')
        page_number = self.request.GET.get('page')
        paginator = Paginator(videos, 4)
        context['videos'] = paginator.get_page(page_number)
        posts = Post.objects.filter(posted_to=video).order_by('-created_at')
        post_page_number = self.request.GET.get('post_page')
        post_paginator = Paginator(posts, 4)
        context['posts'] = post_paginator.get_page(post_page_number)
        context['comments'] = Comment.objects.all().order_by('-created_at')
        if 'resident_id' in self.request.session:
            resident = get_object_or_404(Resident, pk=self.request.session['resident_id'])
            context['resident'] = resident
            if resident in video.resident_like.all():
                context['is_liked'] = True
            else:
                context['is_liked'] = False
        return context

    def post(self, request, *args, **kwargs):
        if len(request.POST['post']) < 15:
            return JsonResponse({'error': 'Please enter your post at least 15 charactors'})
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
        posts = Post.objects.filter(posted_to=video).order_by('-created_at')
        post_page_number = self.request.GET.get('post_page')
        post_paginator = Paginator(posts, 4)
        posts = post_paginator.get_page(post_page_number)
        context = {
            'posts': posts,
            'comments': Comment.objects.all().order_by('-created_at'),
        }
        html = render_to_string('partial/post.html', context, request=request)
        return JsonResponse({'html': html})

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

def add_like(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if 'resident_id' in request.session:
        resident = get_object_or_404(Resident, pk=request.session['resident_id'])
        video.resident_like.add(resident)
        video.save()
    context = {
        'is_liked': True,
        'video': video,
    }
    html = render_to_string('partial/like.html', context, request=request)
    return JsonResponse({'html': html})

def remove_like(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if 'resident_id' in request.session:
        resident = get_object_or_404(Resident, pk=request.session['resident_id'])
        video.resident_like.remove(resident)
        video.save()
    context = {
        'is_liked': False,
        'video': video,
    }
    html = render_to_string('partial/like.html', context, request=request)
    return JsonResponse({'html': html})

def add_description(request, pk):
    if request.method == 'POST':
        if len(request.POST['description']) < 15:
            return JsonResponse({'error': 'Please enter your description at least 15 charactors'})
        else:    
            video = get_object_or_404(Video, pk=pk)
            video.description = request.POST['description']
            video.save()
            return JsonResponse({'description': video.description})

class ResidentLoginView(FormView):
    template_name = 'registration/resident_login.html'
    form_class = ResidentLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['community'] = get_object_or_404(Community, pk=self.kwargs['community_id'])
        return context
    
    def form_valid(self, form):
        community = get_object_or_404(Community, pk=self.kwargs['community_id'])
        print(self.request.POST['password'])
        if check_password(self.request.POST['password'], community.password):
            residents = Resident.objects.filter(community=community)
            for resident in residents:
                if resident.name == self.request.POST['name']:
                    self.request.session.flush()
                    self.request.session['resident_id'] = resident.id
                    self.request.session['community_id'] = community.id
                    return redirect('home', community.id)
            print('the username does not exist')
            return redirect('resident_login', self.kwargs['community_id'])
        else:
            print('wrong password')
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['community'] = get_object_or_404(Community, pk=self.request.session['community_id'])
        context['communities'] = Community.objects.filter(owner=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        request.session['community_id'] = self.request.POST['community_id']
        return redirect('manage_resident')

def delete_resident(request, resident_id):
    resident = get_object_or_404(Resident, pk=resident_id)
    resident.delete()
    return redirect('manage_resident')

def set_admin(request, resident_id):
    if request.method == 'POST':
        resident = get_object_or_404(Resident, pk=resident_id)
        resident.is_staff = request.POST['admin']
        resident.save()
    return redirect('manage_resident')

class VideoListView(ListView):
    model = Video
    template_name = 'list.html'
    context_object_name = 'videos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super(VideoListView, self).get_queryset()
        communities = Community.objects.filter(owner=self.request.user)
        queryset = Video.objects.filter(community__in=communities)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        community = get_object_or_404(Community, pk=self.request.session['community_id'])
        context['community'] = community
        context['communities'] = Community.objects.filter(owner=self.request.user)
        return context

def edit_video_community(request, pk):
    if request.method == 'POST':
        edit_video = get_object_or_404(Video, pk=pk)
        new_community = get_object_or_404(Community, pk=request.POST['community'])
        edit_video.community = new_community
        edit_video.save()
        context = {
            'video': edit_video,
        }
        html = render_to_string('partial/selection.html', context, request=request)
        return JsonResponse({'html': html})

def edit_video_group(request, pk):
    if request.method == 'POST':
        edit_video = get_object_or_404(Video, pk=pk)
        new_group = get_object_or_404(VideoGroup, pk=request.POST['group'])
        edit_video.group = new_group
        edit_video.save()
        return JsonResponse({'success': True})

def edit_video_title(request, pk):
    if request.method == 'POST':
        edit_video = get_object_or_404(Video, pk=pk)
        edit_video.title = request.POST['title']
        edit_video.save()
        return JsonResponse({'success': True})

def edit_video_url(request, pk):
    if request.method == 'POST':
        edit_video = get_object_or_404(Video, pk=pk)
        url = convert_ytframe(request.POST['url'])
        edit_video.url = url
        edit_video.save()
        return JsonResponse({'url': url})

def edit_video_delete(request, pk):
    if request.method == 'POST':
        edit_video = get_object_or_404(Video, pk=pk)
        edit_video.delete()
        return JsonResponse({'success': True})
        