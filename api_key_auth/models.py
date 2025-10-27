import secrets
import hashlib
from django.db import models, IntegrityError
from django.utils import timezone
# Create your models here.


def _hash_key(key: str) -> str:
    return hashlib.sha256(key.encode('utf-8')).hexdigest()

class APIKey(models.Model):
    name = models.CharField(max_length=100, help_text="Human name")
    hashed_key = models.CharField(max_length=64, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    revoked = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({'revoked' if self.revoked else 'active'})"

    @classmethod
    def create_key(cls, name: str, notes:  str = ""):
        MAX_RETRIES = 5
        # generate a sufficiently random plaintext key
        for _ in range(MAX_RETRIES):
            plaintext = secrets.token_urlsafe(32) # ~43 chars base64-url
            hashed = _hash_key(plaintext)
            try:
                obj = cls.objects.create(name=name, hashed_key=hashed, notes=notes)
                return obj, plaintext
            except IntegrityError:
                continue


    def check_key(self, plaintext: str) -> bool:
        if self.revoked:
            return False 
        return self.hashed_key == _hash_key(plaintext)
    
    def mark_used(self):
        self.last_used_at = timezone.now()
        self.save(update_fields=['last_used_at'])
