from django.urls import path
from .api_views import ProfileListCreateView, ProfileDetailView, VolunteerUpdateView, VolunteerDeleteView

urlpatterns = [
    path("volunteers/", ProfileListCreateView.as_view(), name="volunteer-list"),
    path("volunteers/<int:pk>/", ProfileDetailView.as_view(), name="volunteer-detail"),
    path("volunteers/<int:pk>/update/", VolunteerUpdateView.as_view(), name="volunteer-update"),  #  Update
    path("volunteers/<int:pk>/delete/", VolunteerDeleteView.as_view(), name="volunteer-delete"),  # Delete
]



'''
1. Create a Profile (POST)
 
    Endpoint: /api/profiles/
    Process:
        The ProfileListCreateView handles the POST request.
        The ProfileSerializer creates the User and Profile objects.
        Passwords are hashed before saving for security.
 
2. Retrieve a Profile (GET)
 
    Endpoint: /api/profiles/<id>/
    Process:
        The ProfileDetailView handles the GET request.
        Retrieves the profile instance by its id (<id>).
        Returns the serialized profile data, including nested user information.
 
3. Update a Profile (PUT or PATCH)
 
    Endpoint: /api/profiles/<id>/
    Process:
        The ProfileDetailView handles the PUT or PATCH request.
        Updates fields in the Profile and User objects based on the data provided in the request.
 
4. Delete a Profile (DELETE)
 
    Endpoint: /api/profiles/<id>/
    Process:
        The ProfileDetailView handles the DELETE request.
        Deletes the specified Profile instance, including its linked User.
 
'''