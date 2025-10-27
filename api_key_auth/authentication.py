from rest_framework import authentication, exceptions
from django.utils.translation import gettext_lazy as _
from .models import APIKey
import hashlib


class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    Accepts:
      - Authorization: Api-Key <key>
      - or X-API-KEY: <key>
    """

    keyword = "Api-Key"

    def authenticate(self, request):
        # Get key from header
        auth_header = authentication.get_authorization_header(request).decode('utf-8')
        key = None 
        if auth_header:
            parts = auth_header.split(" ")
            if len(parts) == 2 and parts[0] == self.keyword:
                key = parts[1] 
            elif len(parts) == 1 and parts[0].startswith(self.keyword):
                key = parts[0][len(self.keyword):]

        # 2) Fallback to custom header.
        if not key:
            key = request.META.get("HTTP_X_API_KEY") or request.META.get("X_API_KEY")

        if not key:
            raise exceptions.AuthenticationFailed(_("API key required"))

        hashed = hashlib.sha256(key.encode("utf-8")).hexdigest()
        api_key = APIKey.objects.filter(hashed_key=hashed, revoked=False).first()
        if not api_key:
            raise exceptions.AuthenticationFailed(_("Invalid or revoked API key"))

        api_key.mark_used()

        from django.contrib.auth.models import AnonymousUser
        user = AnonymousUser()
        user.username = f"apikey:{api_key.name}"
        return (user, None)
