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


class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

    product_id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, db_column='business_id', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='M')
    color = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return f"{self.name} ({self.sku})"


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
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=150)
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    delivery_status = models.CharField(max_length=100, default='Preparing')
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'

    def save(self, *args, **kwargs):
        if self.pk:
            kwargs['update_fields'] = [
                'product_name', 'size', 'color', 'quantity', 'unit_price', 'status', 'delivery_status'
            ]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_id} - {self.product_name}"