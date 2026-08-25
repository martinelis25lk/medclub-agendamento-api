from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsInternoOrReadOnly(BasePermission):
    """
    Permite leitura (GET, HEAD, OPTIONS) para qualquer usuário (ou clientes autenticados),
    mas restringe alterações (POST, PUT, DELETE) apenas para usuários com role 'interno'.
    """
    def has_permission(self, request, view):
        # Métodos seguros (GET) são permitidos para todos
        if request.method in SAFE_METHODS:
            return True
        
        # Para criar/editar/deletar, o usuário deve estar autenticado E ser do tipo 'interno'
        return request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == 'interno'