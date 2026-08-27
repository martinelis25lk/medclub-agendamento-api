from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsInternoOrReadOnly(BasePermission):
    """
    Permite leitura (GET, HEAD, OPTIONS) para qualquer usuário,
    mas restringe alterações (POST, PUT, DELETE) apenas para usuários com role 'interno'.
    """
    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS:
            return True

        
        return request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == 'interno'