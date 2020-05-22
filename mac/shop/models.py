from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=30,default="")
    subcategory = models.CharField(max_length=30,default="")
    desc = models.CharField(max_length=300)
    price = models.IntegerField(default=0)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images',default='')

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default="")
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=30,default="")
    desc = models.CharField(max_length=300,default="")


    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_Json = models.CharField(max_length=5000, default="")
    total_price = models.CharField(max_length=100,default="")
    name = models.CharField(max_length=50,default="")
    email = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    zip_code = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=30,default="")

    def __str__(self):
        return self.name

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000, default="")
    timestamp = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.update_desc[0:7] + "..."

class Media(models.Model):
    m_id = models.AutoField(primary_key=True)
    audiofile = models.FileField(upload_to='musics/')
    videofile = models.FileField(upload_to='videos/')
    youtube = models.URLField(max_length=200)
    file1 = models.FileField(upload_to='pdf/')

