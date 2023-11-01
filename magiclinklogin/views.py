import os

from django.contrib.auth import authenticate, login
from django.core import signing
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.http import urlencode
from dotenv import load_dotenv
from rest_framework import exceptions, permissions, status, views
from rest_framework.response import Response

from magiclinklogin.serializers import MagicLinkSerializer

load_dotenv()


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    # (TODO): Implement get method to route to redirect to a confirm token page
    # which have a form to call the below POST method

    def post(self, request):
        """
        Verifies if a token is valid and authenticates a user.
        """
        try:
            user = authenticate(request)
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        except exceptions.AuthenticationFailed as error:
            return Response(
                data={"error_message": error.detail},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class MagicLinkView(views.APIView):
    # This view should be accessiable also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """
        Generates a Magic link and sends an email to the provided email
        """
        serializer = MagicLinkSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        magic_link_data = {
            "email": serializer.validated_data["email"],
        }
        if "name" in serializer.validated_data:
            magic_link_data["name"] = (serializer.validated_data["name"],)
        if "group_id" in serializer.validated_data:
            magic_link_data["group_id"] = serializer.validated_data["group_id"]

        # Create magic link
        token = signing.dumps(magic_link_data)
        qs = urlencode({"token": token})
        # (TODO): Edit this url to route to a token confirmation page
        # (TODO): Format this email HTML to be styled
        magic_link = request.build_absolute_uri(location=reverse("login")) + f"?{qs}"
        send_mail(
            "Login Link",
            f'Click <a href="{magic_link}">here</a> to login',
            os.environ.get("EMAIL_HOST_USER"),
            [magic_link_data["email"]],
        )
        return Response(status=status.HTTP_202_ACCEPTED)
