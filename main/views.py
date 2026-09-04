from django.shortcuts import render, redirect, get_object_or_404
from .models import Business, Customer, Order


def index(request):
    if request.method == 'POST':
        business_id = request.POST.get('business_id')
        customer_id = request.POST.get('customer_id')
        product_name = request.POST.get('product_name')
        size = request.POST.get('size')
        color = request.POST.get('color')
        
        # Safely parse numeric inputs
        raw_quantity = request.POST.get('quantity')
        quantity = int(raw_quantity) if raw_quantity else 1

        raw_price = request.POST.get('unit_price')
        unit_price = float(raw_price) if raw_price else 0.0

        # MySQL calculates total_amount automatically as a generated column
        Order.objects.create(
            business_id=business_id,
            customer_id=customer_id,
            product_name=product_name,
            size=size,
            color=color,
            quantity=quantity,
            unit_price=unit_price,
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
    return render(request, 'main/index.html', context)


def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        order.product_name = request.POST.get('product_name')
        order.size = request.POST.get('size')
        order.color = request.POST.get('color')

        raw_quantity = request.POST.get('quantity')
        order.quantity = int(raw_quantity) if raw_quantity else 1

        raw_price = request.POST.get('unit_price')
        order.unit_price = float(raw_price) if raw_price else 0.0

        order.status = request.POST.get('status', order.status)
        
        # Explicitly list only mutable fields so MySQL can generate total_amount natively
        order.save(update_fields=['product_name', 'size', 'color', 'quantity', 'unit_price', 'status'])
        return redirect('index')

    context = {
        'order': order,
        'businesses': Business.objects.all(),
        'customers': Customer.objects.all(),
    }
    return render(request, 'main/order_form.html', context)


def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('index')
    return render(request, 'main/order_confirm_delete.html', {'order': order})