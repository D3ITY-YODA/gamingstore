from django.shortcuts import render

def checkout(request):
    return render(request, 'payments/checkout.html')

def payment_success(request):
    return render(request, 'payments/success.html')

def payment_cancel(request):
    return render(request, 'payments/cancel.html')