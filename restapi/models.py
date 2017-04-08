from django.db import models

import bcrypt


class Account(models.Model):
    """
    Generally each user holds one account
    """

    creation_date = models.DateTimeField()
    enabled = models.BooleanField(default=True)

    name = models.CharField(max_length=64)
    passwordhash = models.CharField(max_length=64)

    # Balance in cents
    balance = models.IntegerField(default=0)

    def set_password(self, password):
        self.passwordhash = bcrypt.hashpw(password, bcrypt.gensalt())

    def verify_password(self, password):
        return password == bcrypt.checkpw(password, self.passwordhash)


class Token(models.Model):
    """
    Token that is used to identify the account. Can be multiple
    """
    creation_date = models.DateTimeField()

    serialhash = models.CharField(max_length=64)
    account = models.ForeignKey(Account)


class Transaction(models.Model):
    """
    Record happened transactions
    """
    date = models.DateTimeField()

    amount = models.IntegerField()
    account = models.ForeignKey(Account)
