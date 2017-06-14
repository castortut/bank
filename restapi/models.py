from django.db import models

import bcrypt
import hashlib


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

    def __str__(self):
        return "Account: " + self.name + "(" + str(self.balance) + ")"

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
    account = models.ForeignKey(Account, null=True)

    @staticmethod
    def find_token(serial):
        needle_hash = Token.hash_token(serial)
        return Token.objects.filter(serialhash=needle_hash).first()

    @staticmethod
    def hash_token(serial):
        return hashlib.sha256(serial.encode()).hexdigest()

    def __str__(self):
        return "Token: " + self.serialhash + (" (" + self.account.name + ")" if self.account else "")

    def set_hash(self, serial):
        self.serialhash = self.hash_token(serial)


class Transaction(models.Model):
    """
    Record happened transactions
    """
    date = models.DateTimeField()

    amount = models.IntegerField()
    account = models.ForeignKey(Account)

    message = models.TextField(default="")

    success = models.BooleanField(default=False)

    def __str__(self):
        return "Transaction: " + self.account.name + ", %.2f" % self.amount + ", " + self.message

    def run(self):
        if self.account.balance + self.amount >= 0:
            self.account.balance += self.amount
            self.account.save()
            self.success = True
        else:
            self.success = False

        self.save()
        return self

    def was_success(self):
        return self.success
