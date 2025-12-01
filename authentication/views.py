from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import JsonResponse

User = get_user_model()


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username") or request.data.get("email")
        password = request.data.get("password") or request.data.get("senha")

        if not username or not password:
            return Response({"detail": "Credenciais obrigatórias."}, status=400)

        # Login por email
        if "@" in username:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                return Response({"detail": "Usuário não encontrado"}, status=401)
        else:
            # Login por username
            user = authenticate(username=username, password=password)

        if not user:
            return Response({"detail": "Credenciais inválidas"}, status=401)

        # Tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # Perfil do usuário
        perfil = getattr(user, "perfil", None)

        setor = perfil.setor if perfil else None
        cargo = perfil.cargo if perfil else None

        # Resposta JSON + cookies HTTP-only
        response = JsonResponse({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "setor": setor,
                "cargo": cargo,
            }
        })

        # Cookies seguros (em produção: secure=True)
        response.set_cookie(
            key="access",
            value=str(access),
            httponly=True,
            secure=False,
            samesite="None",
        )

        response.set_cookie(
            key="refresh",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="None",
        )

        return response

class LogoutView(APIView):
    """
    Se você quiser invalidar refresh tokens, você pode receber o refresh e blacklistear.
    (Requer configuração do blacklist no simplejwt se quiser usar.)
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # front deverá remover token do storage. Se usar blacklist, implemente aqui.
        return Response({"detail": "Logout efetuado."}, status=status.HTTP_200_OK)

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class RefreshCookieView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from rest_framework_simplejwt.tokens import RefreshToken, TokenError

        refresh = request.COOKIES.get("refresh")
        if not refresh:
            return Response({"detail": "Sem refresh"}, status=401)

        try:
            refresh_token = RefreshToken(refresh)
            new_access = refresh_token.access_token
        except TokenError:
            return Response({"detail": "Refresh inválido"}, status=400)

        response = JsonResponse({"detail": "novo access"})

        response.set_cookie(
            key="access",
            value=str(new_access),
            httponly=True,
            secure=True,
            samesite="None",
        )

        return response

