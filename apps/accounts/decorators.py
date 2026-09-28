from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles):
    def check(user):
        return user.is_authenticated and user.role in allowed_roles
    return user_passes_test(check)
