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


# Will be removed and randomized before production
DEVEL_SALT = b'$2b$12$YEXaMZIuPcmlXMM.HSlMOOxUtHbakexjGK7zlQD8JVfz7aUVsAMqW'


class Token(models.Model):
    """
    Token that is used to identify the account. Can be multiple
    """
    creation_date = models.DateTimeField()

    serialhash = models.CharField(max_length=64)
    account = models.ForeignKey(Account)

    @staticmethod
    def find_token(serial):
        hash = Token.hash_token(serial)
        return Token.objects.filter(serialhash=hash).first()


    @staticmethod
    def hash_token(serial):
        return bcrypt.hashpw(serial, DEVEL_SALT)

    def set_hash(self, serial):
        self.serialhash = self.hash_token(serial)


class Transaction(models.Model):
    """
    Record happened transactions
    """
    date = models.DateTimeField()

    amount = models.IntegerField()
    account = models.ForeignKey(Account)
