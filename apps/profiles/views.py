from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, CreateView
from .models import UserProfile
from .forms import ProfileForm, CustomRegisterForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.templatetags.static import static
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

def profile(request):
    return render(request, "profiles/profile.html")

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'dashboard/dashboard_profile.html'
    success_url = reverse_lazy('dashboard_profile')
    
    def get_object(self, queryset = None):
        return self.request.user.userprofile
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['profile'] = profile
        context['profile_picture'] = profile.avatar.url if profile.avatar else static("assets/images/default-game-cover.png")
        context['banner_picture'] = profile.banner.url if profile.banner else static("assets/images/default-game-cover.png")
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Tu perfil se ha actualizado correctamente.")
        return super().form_valid(form)
    
    
class RegisterView(CreateView):
    form_class = CustomRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("public:games_list")
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)
    

class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'dashboard/dashboard_change_password.html'
    success_url = reverse_lazy('change_password')
    success_message = "Contraseña actualizada correctamente."