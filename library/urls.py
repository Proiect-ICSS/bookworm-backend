from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    UserViewSet,
    CategoryViewSet,
    BookViewSet,
    LoanViewSet,
    WaitlistViewSet,
    ReviewViewSet,
    NewsViewSet,
    InfoPageViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"books", BookViewSet)
router.register(r"loans", LoanViewSet)
router.register(r"waitlist", WaitlistViewSet)
router.register(r"reviews", ReviewViewSet)
router.register(r"news", NewsViewSet)
router.register(r"info", InfoPageViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", obtain_auth_token, name="api_token_auth"),
]
