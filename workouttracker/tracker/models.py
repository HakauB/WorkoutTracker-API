from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser, PermissionsMixin
from django.utils import timezone

from guardian.mixins import GuardianUserMixin

# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user =  self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, GuardianUserMixin, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    height = models.IntegerField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    #def get_absolute_url(self):
    #    return "/users/%i/" %(self.pk)


class UserWeight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_weights')
    weight = models.FloatField()
    date = models.DateField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.weight) + ' @ ' + str(self.date)


class ExerciseType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'exercise_type'
        verbose_name = 'Exercise Type'
        verbose_name_plural = 'Exercise Types'
    

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    name = models.CharField(max_length=100)
    date_performed = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'workout'
        verbose_name = 'Workout'
        verbose_name_plural = 'Workouts'


class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_performed = models.DateField()
    exercise_type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    
    class Meta:
        db_table = 'exercise'
        verbose_name = 'Exercise'
        verbose_name_plural = 'Exercises'


class ExerciseSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_performed = models.DateField()
    exercise_type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE, related_name='exercise_sets')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exercise_sets')
    reps = models.IntegerField()
    weight = models.FloatField()
    percentage = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'exercise_set'
        verbose_name = 'Exercise Set'
        verbose_name_plural = 'Exercise Sets'


###############################################################################
#                                JOIN MODELS                                  #
###############################################################################

class OneRepMax(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE)
    weight = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'one_rep_max'
        verbose_name = 'One Rep Max'
        verbose_name_plural = 'One Rep Maxes'