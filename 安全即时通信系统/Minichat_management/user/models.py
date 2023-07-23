from django.db import models


class user(models.Model):
    username = models.CharField(max_length=255, blank=True, primary_key=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255,blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'User_Register'

