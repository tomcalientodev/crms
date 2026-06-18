from django.db import models
from accounts.models import User



# class RecentlyViewed(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='recent_cust' )
#     user_two = models.CharField( max_length=20, blank=True, null=True, )
#     created_at = models.DateTimeField(auto_now=True, null=True,)




# class LastVisitedMiddleware(object):
#     """Set the five last visited url's as session field's, to later display in a recently viewed box."""
#     def process_request(self, request):
#         """Intercept the request and add the current path to it"""
#         request_path = request.get_full_path()
#         try:
#             """If less than six session are stored add a new session url"""
#             if request.session['currently_visiting'] < 5:
#                 request.session['last_visited'] = request.session['currently_visiting']
#             else: 
#                 """Deleted oldest session key and add the newest"""
#                 del request.session['last_visited'][5]
#                 request.session['last_visited'] = request.session['currently_visiting']
#         except KeyError:
#             # silence the exception - this is the users first request
#             pass
#         request.session['currently_visiting'] = request_path