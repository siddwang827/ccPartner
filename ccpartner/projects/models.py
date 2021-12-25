from django.db import models
from django.db import models

from users.models import Profile
import uuid
# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey( Profile,
                               on_delete=models.SET_NULL,
                               default=None,
                               null=True,
                               blank=True )
                               
    title = models.CharField( max_length=100 )
    description = models.TextField( null=True,
                                    blank=True )
    featured_image = models.ImageField( null=True,
                                        blank=True,
                                        default='default.jpg' )
    modules = models.ManyToManyField( "Module", 
                                      blank=True,
                                      null=True, )

    is_active = models.BooleanField( default=True )

    id = models.UUIDField( default=uuid.uuid4,
                           unique=True,
                           primary_key=True,
                           editable=False )
    created = models.DateTimeField( auto_now_add=True )


    class Meta:
        ordering = ['created']

    def __str__(self) -> str:
        return self.title

    @property 
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = '/images/default.jpg'
        return url




class Module(models.Model):
    name = models.CharField(max_length=100)
    id = models.UUIDField( default=uuid.uuid4,
                           unique=True,
                           primary_key=True,
                           editable=False )
    created = models.DateTimeField( auto_now_add=True )
    
    def __str__(self) -> str:
        return self.name



class Group(models.Model):

    project = models.OneToOneField( Project, 
                                    on_delete=models.CASCADE)
    member_1 = models.ForeignKey( Profile,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  default=None,
                                  related_name='member_1')
    member_2 = models.ForeignKey( Profile,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  default=None,
                                  related_name='member_2')                                                          
    member_3 = models.ForeignKey( Profile,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  default=None,
                                  related_name='member_3')

    is_fulled = models.BooleanField( default=False )

    id = models.UUIDField( default=uuid.uuid4,
                           unique=True,
                           primary_key=True,
                           editable=False )
    created = models.DateTimeField( auto_now_add=True )


    def __str__(self) -> str:
        return self.project.title

    class Meta: 
        ordering = ['created']



    @property
    def check_is_full(self):
        if self.member_1 and self.member_2 and self.member_3:
            self.is_fulled = True
        else:
            self.is_fulled = False
        self.save()

    @property
    def members(self):
        member_list = list()
        if self.member_1:
            member_list.append(self.member_1)
        if self.member_2:
            member_list.append(self.member_2)
        if self.member_3:
            member_list.append(self.member_3)
        return member_list

            
        



class Application(models.Model):
    group = models.ForeignKey( Group,
                               on_delete=models.CASCADE )
    sender = models.ForeignKey( Profile,
                                on_delete=models.CASCADE )
    id = models.UUIDField( default=uuid.uuid4,
                           primary_key=True,
                           unique=True,
                           editable=False )
    created = models.DateTimeField( auto_now_add=True )