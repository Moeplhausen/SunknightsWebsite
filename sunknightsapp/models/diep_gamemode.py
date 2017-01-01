from django.db import models

class DiepGamemode(models.Model):
    name=models.CharField(max_length=30,unique=True)
    diep_isDeleted=models.BooleanField(default=False)


    def __str__(self):
        return self.name

