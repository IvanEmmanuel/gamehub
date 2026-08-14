from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import SupportForm
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage

class SupportView(LoginRequiredMixin, FormView):
    template_name = "support/support.html"
    form_class = SupportForm
    success_url =  reverse_lazy("support")
    
    def form_valid(self, form):
        user = self.request.user
        profile = getattr(user, "userprofile", None)
        
        
        info = {
            "subject": form.cleaned_data["subject"],
            "message": form.cleaned_data["message"],
            "user_full_name": user.get_full_name() or user.username,
            "user_email": user.email,
        }
        
        body = render_to_string("support/emails/support_email.txt", info)
        
        #       atributo del settings.py    SUPPORT_INBOX
        to_email = getattr(settings, "SUPPORT_INBOX", None)
        
        if not to_email:
            messages.error(self.request, "No esta configurado el buzon de soporte.")
            return self.form_invalid(form)
        
        try:
            support_email = EmailMessage(
                subject=f"[Soporte] {info['subject']}",
                body= body,
                from_email= getattr(settings, "DEFAULT_FROM_EMAIL", None),
                to = [to_email],
                reply_to= [user.email] if user.email else None
            )
            #email.bcc = [""]
            support_email.send(fail_silently=False)
        except Exception as exc:
            messages.error(self.request, f"No pudimos enviar la solicitud. Intenta mas tarde. Detalle: {type(exc).__name__}: {exc}")
            return self.form_invalid(form)
        
        messages.success(self.request, "¡Tu solicitud de soporte fue enviada!")
        
        return super().form_valid(form)