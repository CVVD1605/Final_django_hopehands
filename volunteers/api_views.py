from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Volunteer
from .serializers import VolunteerSerializer
from .hubspot import create_hubspot_contact  #Import HubSpot function

#  Existing View for Creating and Listing Volunteers
class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [permissions.AllowAny]
    print("Debug: api_views.py loaded")

    def perform_create(self, serializer):
        volunteer = serializer.save(status="approved")  # Automatically approve

        hubspot_response = create_hubspot_contact(volunteer)
        print("HubSpot Response:", hubspot_response)  #  Debugging
# Existing View for Retrieving, Updating, and Deleting a Volunteer
class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Users can read, admins can edit/delete
    print("Debug: api_views.py loaded")

# Admin API to Approve or Reject Volunteers
@api_view(['PATCH'])
@permission_classes([permissions.IsAdminUser])  # Admins only
def approve_volunteer(request, pk):
    try:
        volunteer = Volunteer.objects.get(pk=pk)
    except Volunteer.DoesNotExist:
        return Response({"error": "Volunteer not found"}, status=404)

    status = request.data.get("status")
    if status not in ["approved", "rejected"]:
        return Response({"error": "Invalid status"}, status=400)

    volunteer.status = status
    volunteer.save()

    # Send volunteer to HubSpot if approved
    if status == "approved":
        hubspot_response = create_hubspot_contact(volunteer)
        return Response({
            "message": f"Volunteer {status} successfully",
            "hubspot_response": hubspot_response
        }, status=200)

    return Response({"message": f"Volunteer {status} successfully"}, status=200)
    print("Debug: api_views.py loaded")

# ✅ Update Volunteer Details
class VolunteerUpdateView(generics.UpdateAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can update

# ✅ Delete a Volunteer
class VolunteerDeleteView(generics.DestroyAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can delete