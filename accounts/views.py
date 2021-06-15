from .forms import CustomUserCreateForm
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect

User = get_user_model()

class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('create_community')
    template_name = 'registration/signup.html'
    success_message = 'Thank you for your registration. Please create a community now.'

    def form_valid(self, form):
        #save the new user first
        form.save()
        #get the username and password
        email = self.request.POST['email']
        password = self.request.POST['password1']
        #authenticate user then login
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return redirect(self.success_url)