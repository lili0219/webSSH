from django.db import models
from django.utils import timezone

class DepartMent(models.Model):
    """
    部门表
    """
    name = models.CharField(max_length=64)
    position = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"部门表"

class Employee(models.Model):
    """
    员工信息表
    """
    SEX_CHOICES = (
        (0,"male"),
        (1,"female"),
    )
    ACTIVE_CHOICES = (
        (0,True),
        (1,False),
    )
    name = models.CharField(max_length=32)
    age = models.PositiveIntegerField(null=True,blank=True)
    sex = models.SmallIntegerField(default=0,choices=SEX_CHOICES)
    is_active = models.SmallIntegerField(default=0,choices=ACTIVE_CHOICES)
    department = models.ForeignKey(DepartMent,on_delete=models.CASCADE)

    def __str__(self):
        return "%s:%s"%(self.name,self.department.name)

    class Meta:
        verbose_name_plural = u"员工信息表"
        unique_together = ("employeename","department")

class Duty(models.Model):
    """
    值班表
    """
    NORMAL_CHOICES = (
        (0,"yes"),
        (1,"no")
    )
    name = models.ForeignKey(Employee,on_delete=models.CASCADE)
    department = models.ForeignKey(DepartMent,on_delete=models.CASCADE)
    begintime = models.DateTimeField(default = timezone.now)
    endtime = models.DateTimeField(default = timezone.now)
    date = models.DateTimeField(auto_created=True)
    normal = models.SmallIntegerField(choices=NORMAL_CHOICES,default=0)
    remarks = models.TextField(null=True,blank=True)

    def __str__(self):
        return "%s:%s"%(self.name,self.normal)

    class Meta:
        verbose_name_plural = u"值班表"
