from rest_framework.permissions import BasePermission
from.models import OrganizationOwner, Employee
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


#E.g. use permission_classes = [IsAuthenticated, IsOrganizationOwner] in api classes.

#######BASE PERMISSIONS#########
class IsOrganizationOwner(BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user
            is_organization_owner = OrganizationOwner.objects.filter(user=user).exists()
            if is_organization_owner:
                return True
            else:
                return False
        except Exception as e:
            print("Error checking organization owner:", e)
            raise PermissionDenied("An error occurred while checking organization owner")

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user
            is_employee = Employee.objects.filter(user=user).exists()
            if is_employee:
                return True
            else:
                return False
        except Exception as e:
            print("Error checking employee:", e)
            raise PermissionDenied("An error occurred while checking if user is an employee")

class IsOrganizationOwnerOrEmployee(BasePermission):
    def has_permission(self, request, view):
        from .permissions import IsOrganizationOwner, IsEmployee
        organization_owner = IsOrganizationOwner()
        employee = IsEmployee()
        return organization_owner.has_permission(request, view) or employee.has_permission(request, view)
    

#######PERMISSION ENDPOINTS######

class OrganizationOwnerPermission(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            is_organization_owner = IsOrganizationOwner().has_permission(request, self)
            return JsonResponse({
                    'is_organization_owner': is_organization_owner,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmployeeOwnerPermission(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
             is_employee = IsEmployee().has_permission(request, self)
             return JsonResponse({
                    'is_employee': is_employee,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OwnerEmployeePermission(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            is_organization_owner = IsOrganizationOwner().has_permission(request, self)
            is_employee = IsEmployee().has_permission(request, self)
            return JsonResponse({
                    'is_organization_owner': is_organization_owner,
                    'is_employee': is_employee,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        













   