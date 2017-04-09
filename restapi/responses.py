import datetime

from django.http import JsonResponse


def balance_response(account, balance):
    return JsonResponse({
        'date': datetime.datetime.now().isoformat(),
        'success': True,
        'account': account,
        'balance': balance,
    })


def transaction_response(account, balance):
    return JsonResponse({
        'date': datetime.datetime.now().isoformat(),
        'success': True,
        'account': account,
        'balance': balance,
    })


def error_response(message, message2=None):
    return JsonResponse({
        'date': datetime.datetime.now().isoformat(),
        'success': False,
        'message': message,
        'message2': message2 or ""
    })
