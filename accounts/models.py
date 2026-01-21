from django.db import models
import hashlib
import uuid
from datetime import timedelta
from django.utils import timezone

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    def set_password(self, raw_password):
        self.password = self._hash_password(raw_password)

    def check_password(self, raw_password):
        return self.password == self._hash_password(raw_password)

    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
    

class Session(models.Model):
    session_key = models.CharField(max_length=64, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"Session {self.session_key[:10]}..."
    

    @classmethod
    def create_session(cls, user=None, expired_days=7):
        session_key = uuid.uuid4().hex + uuid.uuid4().hex
        expired_at = timezone.now() + timedelta(days=expired_days)

        session = cls.objects.create(
            session_key=session_key,
            user=user,
            expired_at=expired_at,
        )

        return session
    
    @classmethod
    def get_valid_session(cls, session_key):
        try:
            session = cls.objects.get(session_key=session_key)

            if session.is_expired():
                session.delete()
                return None

            return session
        except cls.DoesNotExist:
            return None

    def is_expired(self):
        return timezone.now() > self.expired_at