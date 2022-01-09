from django.db import models
from django.db import models

from users.models import Profile
import uuid
# Create your models here.

class Project(models.Model):

    FEATURE_TYPE = (
        ("delicacy", "美食評鑑"),
        ("finance", "投資理財"),
        ("sport", '運動健身') ,
        ("pet", "寵物生活"),
        ("toolkit", "輔助工具"),
        ("society", "社會政治"),
        ("shopping", "購物達人"),
        ("entertainment","音樂電影"),
        ("other","其他"),
    )

    owner = models.ForeignKey( Profile,
                               on_delete=models.CASCADE,
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

    types = models.ManyToManyField( "Type", 
                                   blank=True,
                                   null=True,
                                   default=None )

    feature = models.CharField( max_length=20,
                                choices=FEATURE_TYPE,
                                default=FEATURE_TYPE[-1][0] )

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



class Type(models.Model):
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

    is_full = models.BooleanField( default=False )

    id = models.UUIDField( default=uuid.uuid4,
                           unique=True,
                           primary_key=True,
                           editable=False )
    created = models.DateTimeField( auto_now_add=True )


    def __str__(self) -> str:
        return self.project.title

    class Meta: 
        ordering = ['created']


    def addMember(self, profile):
        if not self.member_1:
            self.member_1 = profile
        elif not self.member_2:
            self.member_2 = profile
        else:
            self.member_3 = profile
        self.check_is_full()
        self.save()


    def removeMember(self, profile):
        if self.member_1 == profile:
            self.member_1 = None
        elif self.member_2 == profile:
            self.member_2 = None
        elif self.member_3 == profile:
            self.member_3 = None
        self.check_is_full()
        self.save()

        project = self.project
        project.is_active = True
        project.save()

        profile.group_id = None
        profile.save()

        return



    def check_is_full(self):
        if self.member_1 and self.member_2 and self.member_3:
            self.is_full = True
            # if group is full, hide the project for project list
            project = self.project
            project.is_active = False
            
            project.save()
            
        else:
            self.is_full = False
            
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
    is_apply = models.BooleanField( blank=True, 
                                    null=True )
    id = models.UUIDField( default=uuid.uuid4,
                           primary_key=True,
                           unique=True,
                           editable=False )
    created = models.DateTimeField( auto_now_add=True )

    def __str__(self):
        return f'{self.sender} apply for {self.group.project}'

