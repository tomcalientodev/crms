from django.db import models

from accounts.models import User, Customer



class RecentlyViewedCustomer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)