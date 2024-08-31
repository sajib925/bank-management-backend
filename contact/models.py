from django.db import models


class ContactUs(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=30)
    service_interested = models.CharField(max_length=30)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact Us"