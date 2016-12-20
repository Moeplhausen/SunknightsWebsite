from django.db import models

class Tournament(models.Model):
    name=models.CharField(max_length=20)
    description=models.TextField(max_length=500)
    finished=models.BooleanField(default=False)


    def __str__(self):
        return self.name+": "+self.description