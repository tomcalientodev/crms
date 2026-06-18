from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .models import PasswordReset
from .serializers import RequestPasswordResetSerializer, VerifyResetCodeSerializer, ResetPasswordSerializer

class RequestPasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'detail': 'Email address not found.'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate reset code and send email
            reset_entry = PasswordReset.create_reset_entry(user)
            send_mail(
                'Password Reset Code',
                f'Your reset code is {reset_entry.reset_code}. It will expire in 10 minutes.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response({'detail': 'Reset code sent.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyResetCodeView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = VerifyResetCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            try:
                user = User.objects.get(email=email)
                reset_entry = PasswordReset.objects.get(user=user, reset_code=code)
                if reset_entry.is_expired():
                    return Response({'detail': 'Reset code has expired.'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'detail': 'Code verified.'})
            except (User.DoesNotExist, PasswordReset.DoesNotExist):
                return Response({'detail': 'Invalid code or email.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(email=email)
                reset_entry = PasswordReset.objects.get(user=user, reset_code=code)
                if reset_entry.is_expired():
                    return Response({'detail': 'Reset code has expired.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Validate the new password
                try:
                    validate_password(new_password, user=user)
                except ValidationError as e:
                    return Response({'errors': e.messages}, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(new_password)
                user.save()
                reset_entry.delete()  # Remove the reset entry after password is updated
                return Response({'message': 'success'}, status=status.HTTP_201_CREATED)
            except (User.DoesNotExist, PasswordReset.DoesNotExist):
                return Response({'detail': 'Invalid code or email.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Invalid code or email.'}, status=status.HTTP_400_BAD_REQUEST)



# SAVE BEFORE BETTER ERROR HANDLINGclass ResetPasswordView(APIView):
#     permission_classes = [permissions.AllowAny]
    
#     def post(self, request):
#         serializer = ResetPasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             code = serializer.validated_data['code']
#             new_password = serializer.validated_data['new_password']
#             try:
#                 user = User.objects.get(email=email)
#                 reset_entry = PasswordReset.objects.get(user=user, reset_code=code)
#                 if reset_entry.is_expired():
#                     return Response({'detail': 'Reset code has expired.'}, status=status.HTTP_400_BAD_REQUEST)
                
#                                # Validate the new password
#                 try:
#                     validate_password(new_password, user=user)
#                 except ValidationError as e:
#                     return Response({'detail': e.messages}, status=status.HTTP_400_BAD_REQUEST)

#                 user.set_password(new_password)
#                 user.save()
#                 reset_entry.delete()  # Remove the reset entry after password is updated
#                 return Response({'detail': 'Password reset successfully.'})
#             except (User.DoesNotExist, PasswordReset.DoesNotExist):
#                 return Response({'detail': 'Invalid code or email.'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)