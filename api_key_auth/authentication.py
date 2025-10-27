from rest_framework import authentication, exceptions
from django.utils.translation import gettext_lazy as _
from .models import APIKey


class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    Accepts:
    - Authorization: Api-key <plaintext_key>
    - OR X-API-KEY: <plaintext_key>
    """

    keyword = "Api-Key"

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).decode('utf-8')
        key = None 

        if auth_header:
            parts = auth_header.split()
            if parts == 2 and parts[0] == self.keyword:
                key = parts[1] 
            elif len(parts) == 1 and parts[0].startswith(self.keyword + ":"):
                key = parts[0].split(":", 1)[1]

        # 2) Fallback to custom header.
        if not key:
            key = request.META.get("HTTP_X_API_KEY") or request.META.get("X_API_KEY")
        
        if not key:
            return None 
        
        # Validate against DB
        try:
            # We cannot query by hashed_key without hashing; compute sha256 then query for performance.
            import hashlib 
            hashed = hashlib.sha256(key.encode('utf-8')).hexdigest()
            api_obj = APIKey.objects.filter(hashed_key=hashed, revoked=False).first()
        except Exception:
            raise exceptions.AuthenticationFailed(_("API key authentication error"))
        
        if not api_obj:
            raise exceptions.AuthenticationFailed(_("Invalid or revoked API key"))
        
        # Return an (user, auth) tuple. We don't have Django user per-key; return None user or create a pseudo-user.
        # DRF expects an object; we can return AnonymousUser or a lightweight object.
        from django.contrib.auth.models import AnonymousUser
        return (AnonymousUser(), None)