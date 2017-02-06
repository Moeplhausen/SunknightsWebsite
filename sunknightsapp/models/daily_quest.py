from django.db import models

class DailyQuest(models.Model):
    date = models.DateTimeField(auto_now_add=True,db_index=True)
    task=models.CharField(max_length=500)



    def __str__(self):
            return self.task

