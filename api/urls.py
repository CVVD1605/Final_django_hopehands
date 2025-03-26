from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    UserViewSet,
    LoginView,
    VolunteerListCreateView,
    VolunteerRetrieveUpdateDeleteView,
    VolunteerViewSet,
    HubSpotContactView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'volunteers', VolunteerViewSet, basename='volunteer')

urlpatterns = [
    # Include the router URLs (for viewsets)
    path('', include(router.urls)),  # Authentication endpoint
    # Volunteer API (List & Create)
    path('login/', LoginView.as_view(), name='login'),
    path('volunteers/list-create/', VolunteerListCreateView.as_view(),
         # Volunteer API (Retrieve, Update, Delete)
         name='volunteer-list-create'),
    path('volunteers/<int:pk>/', VolunteerRetrieveUpdateDeleteView.as_view(),
         name='volunteer-detail'),  # HubSpot Contact API
    path('hubspot/create-contact/', HubSpotContactView.as_view(),
         name='hubspot-create-contact'),
]
