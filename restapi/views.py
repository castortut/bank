from django.http import HttpResponse


def view_api_usage(request):
    return HttpResponse("""
    <pre>
    Usage:
    - /api/token/<serial>/balance
      
      Returns your account balance
      
    - /api/token/<serial>/transaction
    
      POST request to make a new transaction
    </pre>
    """)


def view_token_balance(request, token_serial):
    return HttpResponse("Balance: 123.00")


def view_token_transaction(request, token_serial):
    return HttpResponse("Transaction Failed")


def view_hello(request):
    return HttpResponse("Hello")
