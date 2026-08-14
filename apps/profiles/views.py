from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from .models import UserProfile
from .forms import ProfileForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.templatetags.static import static

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
    