from django.db import models

# Create your models here.
class Base(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add = True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now_add = True)

    class Meta:
        abstract = True

class Expense(Base):
    category = models.CharField(max_length = 100)
    date = models.DateField()
    amount = models.FloatField()
    comments = models.CharField(max_length = 100)
    reciept = models.ImageField(blank = True, null = True)

    class Meta:
        managed = True
        db_table = "expenses"
    
    def __str__(self):
        return f"{self.amount} spent in {self.category}"