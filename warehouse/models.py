from django.db import models


class Seller(models.Model):
    identification_number = models.IntegerField()


class Station(models.Model):
    number = models.IntegerField()
    

# class Warehouse(models.Model):
#     name = models.CharField(max_length=200)
#     is_station = models.BooleanField(default=False)


class Provider(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# class Offer(models.Model):
#     consumables = models.ForeignKey(Consumables, on_delete=models.CASCADE)
#     provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=False)
#     cost = models.FloatField(default=0)
#     is_actual = models.BooleanField(default=True)
#
#     warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.consumables


# def get_cost_price(self):
#     sum_price = 0
#     for ingredient in self.ingredient_set.all():
#         consumables_price = Offer.objects.get(consumables__ingredient=ingredient, is_actual=True).cost
#         ingredient_price = ingredient.quantity * consumables_price / ingredient.consumables.size
#         sum_price += ingredient_price
#     return sum_price


# product which has a button in tha application
class Product(models.Model):
    name = models.CharField(max_length=200)
    cost = models.IntegerField(default=0)
    icon = models.ImageField(upload_to="static/img/", verbose_name="Product's icon")

    def __str__(self):
        return self.name


class Consumables(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.FloatField(default=0)
    volume = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    consumables = models.ForeignKey(Consumables, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.consumables)

    def get_available_number(self):
        consumables_quantity = self.consumables.quantity
        available_number = consumables_quantity // self.quantity
        return available_number


class CheckList(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=False)
    check_time = models.DateTimeField()

    def __str__(self):
        return str(self.check_time)

    def summary_price(self):
        return sum([s["price"]*s["quantity"] for s in self.sale_set.values("price", "quantity")])


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    quantity = models.SmallIntegerField(default=0, null=False)
    price = models.IntegerField()

    check_list = models.ForeignKey(CheckList, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s %s" % (self.product, self.quantity)

    def save(self, *args, **kwargs):
        for ingredient in self.product.ingredient_set.all():
            consumables = ingredient.consumables
            consumables.quantity -= ingredient.quantity
            consumables.save()

        super().save(*args, **kwargs)
