from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from .models import Volunteer
from .serializers import VolunteerSerializer, UserSerializer
from services.hubspot_service import HubSpotService
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class LoginView(APIView):
    # permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'},
                        status=status.HTTP_400_BAD_REQUEST)


class VolunteerListCreateView(generics.ListCreateAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    # permission_classes = [permissions.IsAuthenticated] - Creating a new volunteer doesn't require authentication
    # permission_classes =  permissions.AllowAny
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [permissions.IsAuthenticated()]  # Require authentication for listing
    #     return [permissions.AllowAny()]  # Allow anyone to create a volunteer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                # Create volunteer in local database
                volunteer = serializer.save(user=self.request.user)

                # Create contact in HubSpot
                hubspot_service = HubSpotService()
                hubspot_data = {
                    "email": volunteer.email,
                    "first_name": volunteer.first_name,
                    "last_name": volunteer.last_name,
                    "phone": volunteer.phone,
                    "role": volunteer.role,
                    "availability": volunteer.availability
                }

                hubspot_response = hubspot_service.create_contact(hubspot_data)

                # Update volunteer with HubSpot ID
                volunteer.hubspot_id = hubspot_response.get('id')
                volunteer.save()

                return Response({
                    'message': 'Volunteer registered successfully',
                    'data': serializer.data,
                    'hubspot_id': volunteer.hubspot_id
                }, status=status.HTTP_201_CREATED)

            except ValueError as e:
                logger.error(f"HubSpot integration error: {str(e)}")
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                return Response({
                    'error': 'An unexpected error occurred'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VolunteerRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        volunteer = serializer.save()
        try:
            # Update HubSpot contact if it exists
            if volunteer.hubspot_id:
                hubspot_service = HubSpotService()
                hubspot_data = {
                    "email": volunteer.email,
                    "first_name": volunteer.first_name,
                    "last_name": volunteer.last_name,
                    "phone": volunteer.phone,
                    "role": volunteer.role,
                    "availability": volunteer.availability
                }
                hubspot_service.update_contact(
                    volunteer.hubspot_id, hubspot_data)
        except Exception as e:
            logger.error(f"Error updating HubSpot contact: {str(e)}")
            # Continue without failing the request if HubSpot update fails


class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        volunteer = serializer.save(user=self.request.user)
        try:
            # Create HubSpot contact
            hubspot_service = HubSpotService()
            hubspot_data = {
                "email": volunteer.email,
                "first_name": volunteer.first_name,
                "last_name": volunteer.last_name,
                "phone": volunteer.phone,
                "role": volunteer.role,
                "availability": volunteer.availability
            }
            hubspot_response = hubspot_service.create_contact(hubspot_data)
            volunteer.hubspot_id = hubspot_response.get('id')
            volunteer.save()
        except Exception as e:
            logger.error(f"Error creating HubSpot contact: {str(e)}")
            # Continue without failing the request if HubSpot creation fails


class HubSpotContactView(APIView):
    # permission_classes = [permissions.AllowAny]  # Adjust if needed

    def post(self, request):
        logger.info("HubSpot contact creation request received")

        required_fields = ['email', 'first_name',
                           'last_name', 'phone', 'role', 'availability']
        for field in required_fields:
            if not request.data.get(field):
                return Response(
                    {"error": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            hubspot_service = HubSpotService()
            response = hubspot_service.create_contact(request.data)

            return Response({
                'message': 'Contact created successfully in HubSpot',
                'hubspot_id': response.get('id')
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            logger.error("HubSpot validation error: %s", str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.error(
                "Unexpected error in HubSpot contact creation: %s", str(e))
            return Response(
                {"error": "Failed to create contact. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
