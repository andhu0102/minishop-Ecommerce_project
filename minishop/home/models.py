from django.db import models
from django.urls import reverse


# Create your models here.
class cate(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)


    def get_url(self):
        return reverse('prod_cat', args=[self.slug])

    def __str__(self):
        return self.name

class product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    img = models.ImageField(upload_to='picture')
    desc = models.TextField()
    stock = models.IntegerField()
    available = models.BooleanField()
    price = models.IntegerField()
    date = models.DateField()
    category = models.ForeignKey(cate, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('detail', args=[self.category.slug, self.slug])