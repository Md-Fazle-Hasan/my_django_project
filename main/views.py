from django.shortcuts import render, redirect, get_object_or_404
from .models import Business, Customer, Order

# READ & CREATE: List all orders and process new order creation
def index(request):
    if request.method == 'POST':
        business_id = request.POST.get('business_id')
        customer_id = request.POST.get('customer_id')
        product_name = request.POST.get('product_name')
        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = int(request.POST.get('quantity', 1))
        unit_price = float(request.POST.get('unit_price', 0.0))
        
        # Calculate total amount explicitly
        total_amount = quantity * unit_price

        # Save order to database
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
    # Optimized query to fetch relational business and customer details in one DB hit
    orders = Order.objects.select_related('business', 'customer').order_by('-order_id')
    
    context = {
        'businesses': businesses,
        'customers': customers,
        'orders': orders,
    }
    return render(request, 'main/index.html', context)


# UPDATE: Edit an existing order
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        order.product_name = request.POST.get('product_name')
        order.size = request.POST.get('size')
        order.color = request.POST.get('color')
        order.quantity = int(request.POST.get('quantity', 1))
        order.unit_price = float(request.POST.get('unit_price', 0.0))
        order.status = request.POST.get('status', order.status)
        order.total_amount = order.quantity * order.unit_price
        
        order.save()
        return redirect('index')

    context = {
        'order': order,
        'businesses': Business.objects.all(),
        'customers': Customer.objects.all(),
    }
    return render(request, 'main/order_form.html', context)


# DELETE: Cancel or remove an order
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('index')
    return render(request, 'main/order_confirm_delete.html', {'order': order})