from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Prefetch
from requests import request
from rest_framework import viewsets
from rest_framework import permissions
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin
from guardian.shortcuts import assign_perm, get_objects_for_user

from workouttracker.tracker.models import User, UserWeight, ExerciseType, Workout, Exercise, ExerciseSet
from workouttracker.tracker.serializers import NestedExerciseSerializer, NestedWorkoutSerializer, UserSerializer, UserWeightSerializer, ExerciseTypeSerializer, WorkoutSerializer, ExerciseSerializer, ExerciseSetSerializer

# Create your views here.


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if obj.user == request.user:
            if request.method == 'GET':
                return obj.user.has_perm('tracker.view_' + obj.__class__.__name__.lower())
            elif request.method == 'POST':
                return obj.user.has_perm('tracker.add_' + obj.__class__.__name__.lower())
            elif request.method == 'PUT':
                return obj.user.has_perm('tracker.change_' + obj.__class__.__name__.lower())
            elif request.method == 'DELETE':
                return obj.user.has_perm('tracker.delete_' + obj.__class__.__name__.lower())
        return False


class IsRelatedExerciseTypeOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if obj.exercise_type.user == request.user:
            if request.method == 'GET':
                return obj.exercise_type.user.has_perm('tracker.view_' + obj.exercise_type.__class__.__name__.lower())
            elif request.method == 'POST':
                return obj.exercise_type.user.has_perm('tracker.add_' + obj.exercise_type.__class__.__name__.lower())
            elif request.method == 'PUT':
                return obj.exercise_type.user.has_perm('tracker.change_' + obj.exercise_type.__class__.__name__.lower())
            elif request.method == 'DELETE':
                return obj.exercise_type.user.has_perm('tracker.delete_' + obj.exercise_type.__class__.__name__.lower())
        return False


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserWeightViewSet(viewsets.ModelViewSet):
    queryset = UserWeight.objects.all()
    serializer_class = UserWeightSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        assign_perm('tracker.view_userweight',
                    self.request.user, serializer.instance)
        assign_perm('tracker.add_userweight',
                    self.request.user, serializer.instance)
        assign_perm('tracker.change_userweight',
                    self.request.user, serializer.instance)
        assign_perm('tracker.delete_userweight',
                    self.request.user, serializer.instance)

    def get_queryset(self):
        queryset = get_objects_for_user(
            self.request.user, 'tracker.view_userweight')
        return queryset


class ExerciseTypeViewSet(viewsets.ModelViewSet):
    queryset = ExerciseType.objects.all()
    serializer_class = ExerciseTypeSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    # Assign user as logged-in user and assign permissions
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        assign_perm('tracker.view_exercisetype',
                    self.request.user, serializer.instance)
        assign_perm('tracker.add_exercisetype',
                    self.request.user, serializer.instance)
        assign_perm('tracker.change_exercisetype',
                    self.request.user, serializer.instance)
        assign_perm('tracker.delete_exercisetype',
                    self.request.user, serializer.instance)

    def get_queryset(self):
        queryset = get_objects_for_user(
            self.request.user, 'tracker.view_exercisetype')
        return queryset


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        assign_perm('tracker.view_workout',
                    self.request.user, serializer.instance)
        assign_perm('tracker.add_workout',
                    self.request.user, serializer.instance)
        assign_perm('tracker.change_workout',
                    self.request.user, serializer.instance)
        assign_perm('tracker.delete_workout',
                    self.request.user, serializer.instance)

    def get_queryset(self):
        queryset = get_objects_for_user(
            self.request.user, 'tracker.view_workout')
        return queryset


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        assign_perm('tracker.view_exercise',
                    self.request.user, serializer.instance)
        assign_perm('tracker.add_exercise',
                    self.request.user, serializer.instance)
        assign_perm('tracker.change_exercise',
                    self.request.user, serializer.instance)
        assign_perm('tracker.delete_exercise',
                    self.request.user, serializer.instance)

    def get_queryset(self):
        queryset = get_objects_for_user(
            self.request.user, 'tracker.view_exercise')

        workout = self.request.query_params.get('workout', None)
        if workout is not None:
            queryset = queryset.filter(workout=workout)
        
        exercise_types = self.request.query_params.getlist('exercise_type', None)
        if exercise_types is not None and len(exercise_types) > 0:
            queryset = queryset.filter(exercise_type__in=exercise_types)

        start_date = self.request.query_params.get('start_date', None)
        if start_date is not None:
            queryset = queryset.filter(date_performed__gte=start_date)

        end_date = self.request.query_params.get('end_date', None)
        if end_date is not None:
            queryset = queryset.filter(date_performed__lte=end_date)

        date_performed = self.request.query_params.get('date_performed', None)
        if date_performed is not None:
            queryset = queryset.filter(date_performed=date_performed)
        
        return queryset


class ExerciseSetViewSet(viewsets.ModelViewSet):
    queryset = ExerciseSet.objects.all()
    serializer_class = ExerciseSetSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        assign_perm('tracker.view_exerciseset',
                    self.request.user, serializer.instance)
        assign_perm('tracker.add_exerciseset',
                    self.request.user, serializer.instance)
        assign_perm('tracker.change_exerciseset',
                    self.request.user, serializer.instance)
        assign_perm('tracker.delete_exerciseset',
                    self.request.user, serializer.instance)

    def get_queryset(self):
        queryset = get_objects_for_user(
            self.request.user, 'tracker.view_exerciseset')
        exercise = self.request.query_params.get('exercise', None)
        if exercise is not None:
            queryset = queryset.filter(exercise=exercise)
        
        exercise_types = self.request.query_params.getlist('exercise_type', None)
        if exercise_types is not None and len(exercise_types) > 0:
            queryset = queryset.filter(exercise_type__in=exercise_types)

        start_date = self.request.query_params.get('start_date', None)
        if start_date is not None:
            queryset = queryset.filter(date_performed__gte=start_date)

        end_date = self.request.query_params.get('end_date', None)
        if end_date is not None:
            queryset = queryset.filter(date_performed__lte=end_date)

        date_performed = self.request.query_params.get('date_performed', None)
        if date_performed is not None:
            queryset = queryset.filter(date_performed=date_performed)

        return queryset


##############################################################################################

class NestedExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = NestedExerciseSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        assign_perm('tracker.view_exercise',
                    self.request.user, serializer.instance)
        assign_perm('tracker.add_exercise',
                    self.request.user, serializer.instance)
        assign_perm('tracker.change_exercise',
                    self.request.user, serializer.instance)
        assign_perm('tracker.delete_exercise',
                    self.request.user, serializer.instance)

    def get_queryset(self):
        queryset = get_objects_for_user(
            self.request.user, 'tracker.view_exercise')

        start_date = self.request.query_params.get('start_date', None)
        if start_date is not None:
            queryset = queryset.filter(date_performed__gte=start_date)

        end_date = self.request.query_params.get('end_date', None)
        if end_date is not None:
            queryset = queryset.filter(date_performed__lte=end_date)

        date_performed = self.request.query_params.get('date_performed', None)
        if date_performed is not None:
            queryset = queryset.filter(date_performed=date_performed)
        
        return queryset


class NestedWorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = NestedWorkoutSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        assign_perm('tracker.view_workout',
                    self.request.user, serializer.instance)
        assign_perm('tracker.add_workout',
                    self.request.user, serializer.instance)
        assign_perm('tracker.change_workout',
                    self.request.user, serializer.instance)
        assign_perm('tracker.delete_workout',
                    self.request.user, serializer.instance)
        
    def get_queryset(self):
        queryset = get_objects_for_user(
            self.request.user, 'tracker.view_workout')

        start_date = self.request.query_params.get('start_date', None)
        if start_date is not None:
            queryset = queryset.filter(date_performed__gte=start_date)

        end_date = self.request.query_params.get('end_date', None)
        if end_date is not None:
            queryset = queryset.filter(date_performed__lte=end_date)

        date_performed = self.request.query_params.get('date_performed', None)
        if date_performed is not None:
            queryset = queryset.filter(date_performed=date_performed)
        
        return queryset
