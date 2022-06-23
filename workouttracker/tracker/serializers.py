from asyncore import read
import re
from requests import request
from rest_framework import serializers
from guardian.shortcuts import get_objects_for_user
from workouttracker.tracker.models import User, UserWeight, ExerciseType, Workout, Exercise, ExerciseSet


class ExerciseTypePKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return get_objects_for_user(user, 'tracker.view_exercisetype')


class ExercisePKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return get_objects_for_user(user, 'tracker.view_exercise')


class WorkoutPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return get_objects_for_user(user, 'tracker.view_workout')


#class UserWeightPKField(serializers.PrimaryKeyRelatedField):
#    def get_queryset(self):
#        user = self.context['request'].user
#        return get_objects_for_user(user, 'tracker.view_userweight').first()

#class OrganizationPKField(serializers.PrimaryKeyRelatedField):
#    def get_queryset(self):
#        user = self.context['request'].user
#        return get_objects_for_user(user, 'tracker.view_organization')
#
#
#class OrganizationMembershipPKField(serializers.PrimaryKeyRelatedField):
#    def get_queryset(self):
#        user = self.context['request'].user
#        return get_objects_for_user(user, 'tracker.view_organizationmembership')
#
#
#class UserPKField(serializers.PrimaryKeyRelatedField):
#    def get_queryset(self):
#        #return User.objects.all()
#        user = self.context['request'].user
#        return get_objects_for_user(user, 'tracker.view_user')


###############################################################################


class UserWeightSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserWeight
        fields = ('id', 'weight', 'date',)


###############################################################################


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #user_to_organization = OrganizationMembershipPKField(many=True, read_only=True)
    

    class Meta:
        model = User
        #fields = ('id', 'email', 'user_to_organization',)
        fields = ('pk', 'email', 'height',)


#class OrganizationMembershipSerializer(serializers.HyperlinkedModelSerializer):
#    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
#    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#    class Meta:
#        model = OrganizationMembership
#        fields = ('id', 'user', 'organization', 'role',)
#
#
#class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
#    organization_to_user = OrganizationMembershipPKField(many=True, read_only=True) 
#    #serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#    #OrganizationMembershipPKField(many=True, read_only=True) 
#    #OrganizationMembershipPKField(many=True, read_only=True)
#    class Meta:
#        model = Organization
#        fields = ('id', 'name', 'organization_to_user',)


###############################################################################


class ExerciseTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExerciseType
        fields = ('id', 'name',)


class WorkoutSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Workout
        fields = ('id', 'date_performed', 'name',)


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    exercise_type = ExerciseTypePKField()
    workout = WorkoutPKField()

    class Meta:
        model = Exercise
        fields = ('id', 'date_performed', 'exercise_type', 'workout',)


class ExerciseSetSerializer(serializers.HyperlinkedModelSerializer):    
    exercise_type = ExerciseTypePKField()
    exercise = ExercisePKField()

    class Meta:
        model = ExerciseSet
        fields = ('id', 'date_performed', 'exercise_type', 'exercise', 'reps', 'weight', 'percentage',)


################################################################################

#class NestedExerciseSerializer(serializers.ModelSerializer):
#    exercise_sets = ExerciseSetSerializer(many=True)
#
#    def create(self, validated_data):
#        exercise_sets_data = validated_data.pop('exercise_sets')
#        exercise = Exercise.objects.create(**validated_data)
#        for exercise_set_data in exercise_sets_data:
#            ExerciseSet.objects.create(exercise=exercise, **exercise_set_data)
#        return exercise
#    
#    class Meta:
#        model = Exercise
#        fields = ('id', 'date_performed', 'exercise_type', 'exercise_sets',)
#
#
#class NestedWorkoutSerializer(serializers.ModelSerializer):
#    exercises = NestedExerciseSerializer(many=True)
#    
#    class Meta:
#        model = Workout
#        fields = ('id', 'date_performed', 'name', 'exercises',)