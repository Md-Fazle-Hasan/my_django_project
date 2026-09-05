from django.shortcuts import render, redirect, get_object_or_404
from .models import Business, Customer, Order, Product
from .forms import ProductForm


# 1. Login Screen View
def login_view(request):
    if request.method == 'POST':
        return redirect('dashboard')
    return render(request, 'main/login.html')


# 2. Nexora Dashboard Screen View
def dashboard(request):
    new_orders_count = Order.objects.filter(status='NEW').count()
    processing_count = Order.objects.filter(status='PROCESSING').count()
    delivered_count = Order.objects.filter(status='DELIVERED').count()
    low_stock_count = Product.objects.filter(stock_quantity__lt=5).count()

    recent_orders = Order.objects.select_related('customer', 'product').order_by('-order_id')[:5]
    
    context = {
        'new_orders_count': new_orders_count,
        'processing_count': processing_count,
        'delivered_count': delivered_count,
        'low_stock_count': low_stock_count,
        'recent_orders': recent_orders,
    }
    return render(request, 'main/dashboard.html', context)


# 3. Inventory / Add Product View
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'main/add_product.html', {'form': form})


# 4. Existing CRUD Views
def index(request):
    if request.method == 'POST':
        business_id = request.POST.get('business_id')
        customer_id = request.POST.get('customer_id')
        product_name = request.POST.get('product_name')
        size = request.POST.get('size')
        color = request.POST.get('color')
        
        raw_quantity = request.POST.get('quantity')
        quantity = int(raw_quantity) if raw_quantity else 1

        raw_price = request.POST.get('unit_price')
        unit_price = float(raw_price) if raw_price else 0.0

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

    context = {
        'businesses': Business.objects.all(),
        'customers': Customer.objects.all(),
        'orders': Order.objects.select_related('business', 'customer').order_by('-order_id'),
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
        order.save(update_fields=['product_name', 'size', 'color', 'quantity', 'unit_price', 'status'])
        return redirect('index')

    return render(request, 'main/order_form.html', {'order': order, 'businesses': Business.objects.all(), 'customers': Customer.objects.all()})


def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('index')
    return render(request, 'main/order_confirm_delete.html', {'order': order})