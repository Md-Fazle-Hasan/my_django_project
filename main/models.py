from django.db import models


class Business(models.Model):
    business_id = models.AutoField(primary_key=True)
    business_name = models.CharField(max_length=150)
    owner_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'businesses'

    def __str__(self):
        return self.business_name


class User(models.Model):
    ROLE_CHOICES = [
        ('OWNER', 'Owner'),
        ('STAFF', 'Staff'),
    ]

    user_id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, db_column='business_id')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STAFF')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.name} ({self.role})"


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, db_column='business_id')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    messenger_id = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('CONFIRMED', 'Confirmed'),
        ('PROCESSING', 'Processing'),
        ('READY_FOR_DELIVERY', 'Ready for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, db_column='business_id')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customer_id')
    product_name = models.CharField(max_length=150)
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Read-only field mapped to MySQL generated column
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"Order #{self.order_id} - {self.product_name}"

    class Meta:
        db_table = 'orders'

    def save(self, *args, **kwargs):
        # Automatically calculate total_amount before saving to DB
        self.total_amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_id} - {self.product_name}"