from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("villa/", views.detail, {"slug":"villa"}, name="villa"),
    path("explore-villa/", views.detail, {"slug":"villa"}),
    path("rooms/", views.detail, {"slug":"rooms"}, name="rooms"),
    path("activities/", views.detail, {"slug":"activities"}, name="activities"),
    path("about/", views.detail, {"slug":"story"}, name="story"),
    path("our-story/", views.detail, {"slug":"story"}),
    path("contact/", views.contact, name="contact"),
    path("cookie-policy/", views.policy, {"kind":"cookie"}, name="cookie-policy"),
    path("privacy-policy/", views.policy, {"kind":"privacy"}, name="privacy-policy"),
    path("terms-and-conditions/", views.policy, {"kind":"terms"}, name="terms"),
]
