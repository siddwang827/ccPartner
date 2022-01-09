from django.db.models import fields
from rest_framework import serializers
from projects.models import Project, Group, Module
from users.models import Profile

# Project related model

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        exclude = ['id', "created"]


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username',)


class GroupSerializer(serializers.ModelSerializer):
    member_1 = MemberSerializer(many=False)
    member_2 = MemberSerializer(many=False)
    member_3 = MemberSerializer(many=False)

    class Meta:
        model = Group
        exclude = [
            'id', 
            'created',
            'project',
        ]



# User related model
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['created']




class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    modules = ModuleSerializer(many=True)
    group = GroupSerializer(many=False)

    class Meta:
        model = Project
        exclude = [
            'created'
        ]


    def get_group(self, obj):
        group = obj.group

        serializer = GroupSerializer(group, many=False)
        return serializer.data

    



