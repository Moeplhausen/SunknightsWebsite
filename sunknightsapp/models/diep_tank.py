from django.db import models

class DiepTank(models.Model):
    TIER_OPTIONS=(
        (1,'Tier 1'),
        (2,'Tier 2'),
        (3,'Tier 3'),
        (4,'Tier 4')
    )

    OPNESS_OPTIONS=(
        (1,'Tier 1'),
        (2,'Tier 2'),
        (3,'Tier 3')
    )

    name=models.CharField(max_length=30,unique=True)
    diep_isDeleted=models.BooleanField(default=False)
    opness=models.PositiveSmallIntegerField(choices=OPNESS_OPTIONS,default=OPNESS_OPTIONS[0][0])

    tier=models.PositiveSmallIntegerField(choices=TIER_OPTIONS)

    class Meta:
        ordering = ['name']



    def __str__(self):
        return self.name


class DiepTankInheritance(models.Model):
    parent=models.ForeignKey(DiepTank,null=True,blank=True,on_delete=models.CASCADE)
    me=models.ForeignKey(DiepTank,related_name="inheritance",on_delete=models.CASCADE)


    def __str__(self):
        if self.parent:
            return self.me.name+" < "+self.parent.name
        return self.me.name

    class Meta:
        unique_together=('me','parent')
