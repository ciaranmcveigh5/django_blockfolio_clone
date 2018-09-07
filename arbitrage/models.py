from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username + " - " + self.password


class CryptoAsset(models.Model):
    owner = models.ForeignKey(User, on_delete=(models.CASCADE))
    assetName = models.CharField(max_length=250)
    assetSymbol = models.CharField(max_length=5)
    assetValueAtPurchase = models.FloatField(default=0)
    assetValueNow = models.FloatField(default=0)
