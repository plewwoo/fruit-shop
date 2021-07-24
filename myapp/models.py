from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.


class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profilePic",
                              null=True, blank=True, default="default.jpg")
    userType = models.CharField(max_length=100, default="member")
    cartQty = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


class AllProduct (models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    detail = models.TextField(null=True, blank=True)
    imgUrl = models.CharField(max_length=200, null=True, blank=True)
    instock = models.BooleanField(default=True)
    quantity = models.IntegerField(default=1)
    unit = models.CharField(max_length=200, default="-")
    img = models.ImageField(upload_to="products", null=True, blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    productId = models.CharField(max_length=100)
    productName = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()
    stamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '%s (%s)' % (self.user.first_name, self.productName)


class OrderList(models.Model):
    orderId = models.CharField(max_length=100)
    productId = models.CharField(max_length=100)
    productName = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return self.orderId


class OrderPending(models.Model):
    orderId = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    address = models.TextField()
    shipping = models.CharField(max_length=100)
    payment = models.CharField(max_length=100)
    ps = models.TextField(blank=True, null=True)
    stamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    paid = models.BooleanField(default=False)
    slip = models.ImageField(upload_to="slip", null=True, blank=True)
    # มาเพิ่มเป็น datetime พร้อมกับ calender html
    slipTime = models.CharField(max_length=100, blank=True, null=True)
    paymentId = models.CharField(max_length=100, blank=True, null=True)
    trackingNumber = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.orderId
