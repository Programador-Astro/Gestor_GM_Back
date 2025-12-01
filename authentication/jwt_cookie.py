from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTAuthenticationFromCookie(JWTAuthentication):
    def authenticate(self, request):
        access = request.COOKIES.get("access")

        if not access:
            return None

        raw_token = access
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
