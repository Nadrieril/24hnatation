from django.db import models
from rest_framework import viewsets, serializers
from django.contrib.auth.models import User
from nat24h.utils import VirtualField


class Activity(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __unicode__(self):
        return self.name


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
    _type = VirtualField("Activity")


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer



class Team(models.Model):
    name = models.CharField(max_length=100)
    activity = models.ForeignKey(Activity)
    admin = models.ForeignKey(User, related_name="owned_team_set")
    members = models.ManyToManyField(User)
    # result = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name + " (activity: " + unicode(self.activity) + ", admin: " + unicode(self.admin) + ")"


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
    _type = VirtualField("Team")


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_fields = ['activity', 'members']




class TimeSlot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    value = models.FloatField()

    def __unicode__(self):
        return "slot %s : %s" % (self.start, self.end)


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
    _type = VirtualField("TimeSlot")


class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer



class TimeSlotSubscription(models.Model):
    user = models.ForeignKey(User)
    slot = models.ForeignKey(TimeSlot)
    # result = models.FloatField()


class TimeSlotSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlotSubscription
    _type = VirtualField("TimeSlotSubscription")


class TimeSlotSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = TimeSlotSubscription.objects.all()
    serializer_class = TimeSlotSubscriptionSerializer
    filter_fields = {
        'slot': ['exact'],
        'user': ['exact']}
