from django.db import models
from django.utils import timezone

class Snowboard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    rental_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity_available = models.PositiveIntegerField()
    image = models.ImageField(upload_to='snowboards/', blank=True, null=True)

    def __str__(self):
        return self.name

    def is_available(self):
        return self.quantity_available > 0

class Renter(models.Model):
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    def rent_board(self, snowboard):
        if snowboard.quantity_available > 0:
            Rental.objects.create(snowboard=snowboard, renter=self)
            snowboard.quantity_available -= 1
            snowboard.save()
            return True
        return False

    def return_board(self, rental):
        if rental.renter == self and rental.return_date is None:
            rental.return_date = timezone.now()
            rental.snowboard.quantity_available += 1
            rental.snowboard.save()
            rental.save()
            return True
        return False

    def current_rentals(self):
        return Rental.objects.filter(renter=self, return_date__isnull=True)

    def rental_status(self):
        return self.current_rentals().exists()

class Rental(models.Model):
    snowboard = models.ForeignKey(Snowboard, on_delete=models.CASCADE)
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    rental_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.renter.username} rented {self.snowboard.name}"

    def is_active(self):
        return self.return_date is None
