from asyncore import read
import re
from requests import request
from rest_framework import serializers
from guardian.shortcuts import get_objects_for_user
from workouttracker.tracker.models import User, UserWeight, ExerciseType, Workout, Exercise, ExerciseSet
from guardian.shortcuts import assign_perm


class ExerciseTypePKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return get_objects_for_user(user, 'tracker.view_exercisetype')


class ExerciseSetPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return get_objects_for_user(user, 'tracker.view_exerciseset')


class ExercisePKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return get_objects_for_user(user, 'tracker.view_exercise')


class WorkoutPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return get_objects_for_user(user, 'tracker.view_workout')


class ExerciseSetRelatedField(serializers.RelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return get_objects_for_user(user, 'tracker.view_exerciseset')

    def to_representation(self, value):
        # return dict(id=value.id, reps=value.reps, weight=value.weight, percentage=value.percentage)
        return value


class ExerciseRelatedField(serializers.RelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return get_objects_for_user(user, 'tracker.view_exercise')


class ExerciseTypeRelatedField(serializers.RelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return get_objects_for_user(user, 'tracker.view_exercisetype')


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

class ExerciseSetNestedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExerciseSet
        fields = ('id', 'date_performed', 'reps', 'weight', 'percentage',)


class NestedExerciseSerializer(serializers.ModelSerializer):
    exercise_sets = ExerciseSetNestedSerializer(many=True)

    def create(self, validated_data):
        exercise_sets_data = validated_data.pop('exercise_sets')
        userr = validated_data.pop('user')
        exercise_typee = validated_data.pop('exercise_type')
        exercise = Exercise.objects.create(
            user=userr,
            exercise_type=exercise_typee,
            **validated_data
            )
        assign_perm('tracker.view_exercise', userr, exercise)
        assign_perm('tracker.add_exercise', userr, exercise)
        assign_perm('tracker.change_exercise', userr, exercise)
        assign_perm('tracker.delete_exercise', userr, exercise)
        for exercise_set_data in exercise_sets_data:
            exercise_set = ExerciseSet.objects.create(
                user=userr,
                exercise=exercise,
                exercise_type=exercise_typee, 
                **exercise_set_data
                )
            assign_perm('tracker.view_exerciseset', userr, exercise_set)
            assign_perm('tracker.add_exerciseset', userr, exercise_set)
            assign_perm('tracker.change_exerciseset', userr, exercise_set)
        return exercise
    
    class Meta:
        model = Exercise
        fields = ('id', 'date_performed', 'exercise_type', 'exercise_sets',)


class NestedWorkoutSerializer(serializers.ModelSerializer):
    exercises = NestedExerciseSerializer(many=True)

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        date_performedd = validated_data.pop('date_performed')
        userr = validated_data.pop('user')
        workout = Workout.objects.create(
            user=userr,
            date_performed=date_performedd,
            **validated_data
            )
        assign_perm('tracker.view_workout', userr, workout)
        assign_perm('tracker.add_workout', userr, workout)
        assign_perm('tracker.change_workout', userr, workout)
        assign_perm('tracker.delete_workout', userr, workout)
        for exercise_data in exercises_data:
            exercise_typee = exercise_data.pop('exercise_type')
            exercise_sets_data = exercise_data.pop('exercise_sets')
            exercise = Exercise.objects.create(
                user=userr,
                workout=workout,
                exercise_type=exercise_typee,
                **exercise_data
                )
            assign_perm('tracker.view_exercise', userr, exercise)
            assign_perm('tracker.add_exercise', userr, exercise)
            assign_perm('tracker.change_exercise', userr, exercise)
            assign_perm('tracker.delete_exercise', userr, exercise)
            for exercise_set_data in exercise_sets_data:
                exercise_set = ExerciseSet.objects.create(
                    user=userr,
                    exercise=exercise,
                    exercise_type=exercise_typee,
                    **exercise_set_data
                    )
                assign_perm('tracker.view_exerciseset', userr, exercise_set)
                assign_perm('tracker.add_exerciseset', userr, exercise_set)
                assign_perm('tracker.change_exerciseset', userr, exercise_set)
                assign_perm('tracker.delete_exerciseset', userr, exercise_set)
        return workout

    class Meta:
        model = Workout
        fields = ('id', 'date_performed', 'name', 'exercises',)