from django.db.models.signals import post_save, post_delete
from .models import Group, Project

def createGroup(sender, instance, created, **kwargs):
    print('Group create signal triggered')
    
    if created:
        project = instance
        group = Group.objects.create(
            project=project
        )
        owner = project.owner
        owner.group_id = group.id
        owner.is_host = True
        owner.save()

        print('Your Porject Group is created...')


post_save.connect(createGroup, sender=Project)


def clearOwner(sender, instance, **kwargs):
    project = instance
    owner = project.owner
    owner.group_id = None
    owner.is_host = False
    owner.save()

    print('clear the project owner info...')

post_delete.connect(clearOwner, sender=Project)
