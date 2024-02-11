from django.db import models
from django.utils import timezone

# This model is using for saving the current and updated time and date of the other model instances.
class TimestampModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)  # Manually provide a default value
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


#  This class is made for saving categories in this table.
class Category(TimestampModel):
    category = models.CharField(max_length=50, blank=True, null=True, default="")

    def __str__(self):
        return self.category
    

#  This class is made for saving sub categories in this table.
class SubCategory(TimestampModel):
    category = models.CharField(max_length=50, blank=True, null=True, default="")

    def __str__(self):
        return self.category
    

#  This class is made for saving Product in this table.
class Product(TimestampModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=70, blank=True, null=True)
    size = models.CharField(max_length=32, blank=True, null=True)
    color = models.CharField(max_length=32, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=32, blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True, default=0.0)
    extra_fields = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name