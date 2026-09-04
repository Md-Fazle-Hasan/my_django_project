from django.shortcuts import render, redirect
from .models import Business, Customer, Order

def index(request):
    if request.method == 'POST':
        business_id = request.POST.get('business_id')
        customer_id = request.POST.get('customer_id')
        product_name = request.POST.get('product_name')
        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = int(request.POST.get('quantity', 1))
        unit_price = float(request.POST.get('unit_price', 0))
        
        # Calculate total amount explicitly in Python
        total_amount = quantity * unit_price

        # Save directly to MySQL database
        Order.objects.create(
            business_id=business_id,
            customer_id=customer_id,
            product_name=product_name,
            size=size,
            color=color,
            quantity=quantity,
            unit_price=unit_price,
            total_amount=total_amount,
            status='NEW'
        )
        return redirect('index')

    businesses = Business.objects.all()
    customers = Customer.objects.all()
    orders = Order.objects.select_related('business', 'customer').order_by('-order_id')
    
    context = {
        'businesses': businesses,
        'customers': customers,
        'orders': orders,
    }
    return render(request, 'index.html', context)