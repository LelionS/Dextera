from django.db import models

class House(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Bay(models.Model):
    name = models.CharField(max_length=100)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='bays', null=True)

    def __str__(self):
        return f"{self.house.name} - {self.name}"

class Bed(models.Model):
    bay = models.ForeignKey(Bay, on_delete=models.CASCADE, related_name="beds")
    code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.bay.name} - {self.code}"

class Variety(models.Model):
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, related_name="varieties")
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.bed.code} - {self.name}"

class DataEntry(models.Model):
    bay = models.ForeignKey(Bay, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    amounts = models.IntegerField()
    date = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.bay.name} - {self.bed.code} - {self.variety.name} - {self.amounts}"

from django.contrib.auth.models import User
from django.utils.timezone import now

class WeekEntry(models.Model):
    week = models.CharField(max_length=20)  # e.g., "2025-W09"
    bay = models.ForeignKey(Bay, on_delete=models.CASCADE, default=1)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, default=1)
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE, default=1)
    amounts = models.IntegerField()
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Track who submitted
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.week} - {self.bay.name} - {self.bed.code} - {self.variety.name} - {self.amounts} - {self.submitted_by.username}"