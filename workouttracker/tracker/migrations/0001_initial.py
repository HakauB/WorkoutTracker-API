# Generated by Django 4.0.5 on 2022-06-14 03:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import guardian.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(blank=True, max_length=254, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            bases=(guardian.mixins.GuardianUserMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_performed', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Exercise',
                'verbose_name_plural': 'Exercises',
                'db_table': 'exercise',
            },
        ),
        migrations.CreateModel(
            name='ExerciseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Exercise Type',
                'verbose_name_plural': 'Exercise Types',
                'db_table': 'exercise_type',
            },
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_performed', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workouts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Workout',
                'verbose_name_plural': 'Workouts',
                'db_table': 'workout',
            },
        ),
        migrations.CreateModel(
            name='UserWeight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('delete_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_weights', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='OneRepMax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('exercise_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.exercisetype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'One Rep Max',
                'verbose_name_plural': 'One Rep Maxes',
                'db_table': 'one_rep_max',
            },
        ),
        migrations.CreateModel(
            name='ExerciseSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_performed', models.DateField()),
                ('reps', models.IntegerField()),
                ('weight', models.FloatField()),
                ('percentage', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_sets', to='tracker.exercise')),
                ('exercise_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_sets', to='tracker.exercisetype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Exercise Set',
                'verbose_name_plural': 'Exercise Sets',
                'db_table': 'exercise_set',
            },
        ),
        migrations.AddField(
            model_name='exercise',
            name='exercise_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.exercisetype'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='exercise',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='tracker.workout'),
        ),
    ]
