"""looping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from groups.views import GroupViewSet
from magiclinklogin.views import LoginView, MagicLinkView
from newsletters.views import AnswerViewSet, NewsletterViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register(r"newsletters", NewsletterViewSet, basename="newsletter")
router.register(r"groups", GroupViewSet, basename="group")
router.register(
    r"newsletters/(?P<newsletter_id>[^/.]+)/answers",
    AnswerViewSet,
    basename="newsletter-answers",
)
router.register(r"users", UserViewSet, basename="user")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("magic-link/", MagicLinkView.as_view()),
    path("", include(router.urls)),
]
