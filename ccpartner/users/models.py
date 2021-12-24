from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Profile(models.Model):
    JOB_TYPE = (
        ('student', '學生'),
        ('employed', '在職'),
        ('other', '其他'),
    )

    user = models.OneToOneField( User,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True )
                                 
    name = models.CharField( max_length=100,
                             blank=True,
                             null=True )
    email = models.EmailField( max_length=200,
                               blank=True,
                               null=True )
    username = models.CharField( max_length=200,
                                 blank=True,
                                 null=True )
    bio = models.TextField( blank=True,
                            null=True )
    profile_image = models.ImageField( blank=True,
                                       null=True,
                                       upload_to="profiles/",
                                       default = 'profiles/user-default.png' )
    social_facebook = models.CharField( max_length=200,
                                        blank=True,
                                        null=True )
    location = models.CharField( max_length=100, 
                                 blank=True,
                                 null=True )
    background = models.CharField( max_length=200,
                                   blank=True,
                                   null=True )

    job = models.CharField( max_length=100,
                            choices=JOB_TYPE )

    is_host = models.BooleanField( default=False )

    group_id = models.CharField( max_length=200,
                                 default=None,
                                 blank=True,
                                 null=True )

    created = models.DateTimeField( auto_now_add=True )
    id = models.UUIDField( default=uuid.uuid4,
                           unique=True,
                           primary_key=True,
                           editable=False )
    
    def __str__(self):
        return self.user.username


    @property
    def imageURL(self):
        try: 
            url = self.profile_image.url
        except:
            url = '/images/profiles/user-default.png'
        return url


class Hobby(models.Model):
    owner = models.ForeignKey(Profile, 
                              on_delete=models.CASCADE,
                              null=True, 
                              blank=True)
    name = models.CharField(max_length=200,
                            blank=True,
                            null=True)
    description = models.TextField(blank=True, 
                                   null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField( default=uuid.uuid4,
                           unique=True,
                           primary_key=True,
                           editable=False)
    def __str__(self):
        return str(self.name)