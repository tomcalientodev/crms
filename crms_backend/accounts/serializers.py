from rest_framework import serializers

from .models import User, Customer, Employee, Organization



class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'organization']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'format_phone_number', ]


    def get_formatted_phone_number(self, obj):
        return obj.format_phone_number()

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ['id', 'user', 'organization',  ]

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    organization = OrganizationSerializer()
    class Meta:
        model = Employee
        fields = ['id', 'user', 'organization']

class UserPermissionSerializer(serializers.Serializer):
    is_employee = serializers.BooleanField()
    is_organization_owner = serializers.BooleanField()


class OptionalEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email']
        extra_kwargs = {
            'email': {'required': False}
        }

class updateCustomerSerializer(serializers.ModelSerializer):
    user = OptionalEmailSerializer()
    class Meta:
        model = Customer
        fields = ['id', 'user','organization', ]


##############testing below#############

class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    new_password = serializers.CharField()
