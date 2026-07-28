# signals.py
from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.dispatch import receiver

@receiver(user_logged_in)
def cerrar_sesiones_anteriores(sender, request, user, **kwargs):
    sesiones_activas = Session.objects.filter(expire_date__gte=timezone.now())
    
    for sesion in sesiones_activas:
        data = sesion.get_decoded()
        if data.get('_auth_user_id') == str(user.id) and sesion.session_key != request.session.session_key:
            sesion.delete()