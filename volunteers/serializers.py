from rest_framework import serializers
from .models import Volunteer

class VolunteerSerializer(serializers.ModelSerializer):
    print("Debug: serializers.py loaded")
    class Meta:
        model = Volunteer
        fields = '__all__'
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }
