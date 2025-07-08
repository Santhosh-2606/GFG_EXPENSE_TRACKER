from django.shortcuts import render,redirect
from .models import CurrentBalance,TrackingHistory
from django.contrib import messages

# Create your views here.

def index(request):
    if request.method =='POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        
        current_balance, _ = CurrentBalance.objects.get_or_create(id = 1)
        expense_type = 'CRIDIT'
        if float(amount) < 0:
            expense_type = 'DEBIT'
        
        if float(amount) == 0:
            messages.success(request, "Amount cannot be zero") 
            return redirect('/')

        tracking_history = TrackingHistory.objects.create(current_balance = current_balance, 
            amount = amount,
            description = description, 
            expense_type = expense_type)
        current_balance.current_balance += float(tracking_history.amount)
        current_balance.save()
        return redirect('/')
    
    current_balance, _ =CurrentBalance.objects.get_or_create(id = 1)
    income = 0
    expense = 0
    for tracking_history in TrackingHistory.objects.all():
        if tracking_history.expense_type == 'CRIDIT':
            income += tracking_history.amount
        else:
            expense += tracking_history.amount
    context = {
        'transactions': TrackingHistory.objects.all(),
        'current_balance':current_balance,
        'income':income,
        'expense':expense

    }         
    return render(request,'index.html', context)


def delete_transaction(request,id):
    tracking_history =TrackingHistory.objects.filter(id = id)
    if tracking_history.exists():
        current_balance, _ =CurrentBalance.objects.get_or_create(id = 1)
        tracking_history = tracking_history[0]
        current_balance.current_balance = current_balance.current_balance - tracking_history.amount
        current_balance.save()
    tracking_history.delete()
    return redirect('/')