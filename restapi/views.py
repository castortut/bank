import datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from restapi.responses import balance_response, error_response, transaction_response
from restapi.models import *


def view_api_usage(request):
    return HttpResponse("""
    <pre>
    Usage:
    - /api/token/&lt;serial&gt;/balance
      
      Returns your account balance
      
    - /api/token/&lt;serial&gt;/transaction
    
      POST request to make a new transaction
    </pre>
    """)


def new_token(token_serial):
    token = Token()
    token.creation_date = datetime.datetime.now()
    token.serialhash = Token.hash_token(token_serial)
    token.save()
    return error_response("New token", "Please register")


@csrf_exempt
def view_token_balance(request, token_serial):
    token = Token.find_token(token_serial)
    if token is not None:
        if token.account is not None:
            return balance_response(token.account.name, token.account.balance)
        else:
            return error_response("Token not registered", "Please register")
    else:
        return new_token(token_serial)


@csrf_exempt
def view_token_transaction(request, token_serial):
    token = Token.find_token(token_serial)
    if token is not None:
        if token.account is not None:
            transaction = Transaction(account=token.account, amount=int(request.POST['amount']))
            if transaction.run().was_success():
                return transaction_response(token.account.name, token.account.balance)
            else:
                return error_response("Insufficient balance")
        else:
            return error_response("Token not registered", "Please register")
    else:
        return new_token(token_serial)
