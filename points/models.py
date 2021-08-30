from django.db import models

# Create your models here.
class InterestPoint(models.Model):
    ''' 
        Stores the InterestPoint created by any user
    '''
    name = models.CharField(max_length=100)
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SharedInterest(models.Model):
    ''' 
        Stores the interest points shared between users on the app
    '''
    interest = models.ForeignKey('InterestPoint', on_delete=models.CASCADE)
    shared_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)