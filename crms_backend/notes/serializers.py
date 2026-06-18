
from rest_framework import serializers
from accounts.serializers import UserSerializer, CustomerSerializer

from .models import Note, Job, Customer
from accounts.models import User



# original can delete after editing note feature works class NoteSerializer(serializers.ModelSerializer):
#     created_by = UserSerializer()
#     class Meta:
#         model = Note
#         fields = ['id', 'name', 'body', 'related_customer', 'created_by', 'updated_by', 'created_at_formatted', 'updated_at',  ]


class JobSerializer(serializers.ModelSerializer):
    lead = UserSerializer(read_only=True) #to access the FK in lead.
    lead_two = UserSerializer(read_only=True) 
    related_customer = CustomerSerializer(read_only=True)
    # lead = serializers.UUIDField(source='lead_id')
    class Meta:
        model = Job
        fields = [ 'id', 'name', 'status', 'lead', 'lead_two', 'related_customer', 'due_date',   ]


class NoteSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)  # Make created_by field read-only
    updated_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='updated_by', required=False
    )
    updated_by = UserSerializer(read_only=True)
    related_job = JobSerializer(read_only=True) 

    class Meta:
        model = Note
        fields = ['id', 'name', 'body', 'related_customer', 'related_job',  'created_by', 'updated_by_id', 'updated_by', 'created_at_formatted', 'updated_at']

    def update(self, instance, validated_data):
        # Exclude 'created_by' from validated data during updates
        validated_data.pop('created_by', None)
        # Ensure `updated_by` is set if provided
        if 'updated_by' in validated_data:
            instance.updated_by = validated_data.pop('updated_by')
        return super().update(instance, validated_data)




#TODO: Add to serialization notes in Google Notes: id = serializers.UUIDField(format='hex') this code when added to serialziers'py gets rid of the dashes!








