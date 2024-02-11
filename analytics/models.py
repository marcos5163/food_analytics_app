from django.db import models

class Customer(models.Model):
    
    FOOD_COMPANY = (
        ("SWIGGY", "SWIGGY"),
        ("ZOMATO", "ZOMATO")
    )

    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100)
    food_company_name = models.CharField(max_length=100, choices=FOOD_COMPANY)


class SwiggySessionData(models.Model):
    
    STATE_CHOICES = (
        ("ACTIVE", "ACTIVE"),
        ("EXPIRED", "EXPIRED")
    )

    mobile = models.CharField(max_length=100)
    t_id = models.CharField(max_length=100)
    s_id = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100)
    session_id = models.CharField(max_length=500, null=True)
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default='ACTIVE')


class SwiggyOrderTotal(models.Model):
    mobile = models.CharField(max_length = 100)
    order_total = models.IntegerField()
    num_of_orders = models.IntegerField(null=True)
    last_updated = models.DateTimeField(auto_now = True)
    
    
    
    
    


 
