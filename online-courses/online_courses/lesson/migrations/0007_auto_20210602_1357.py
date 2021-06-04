# Generated by Django 3.2.3 on 2021-06-02 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0006_alter_studentstohomeworks_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentstohomeworks',
            name='homework_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='lesson.homework'),
        ),
        migrations.AlterField(
            model_name='studentstohomeworks',
            name='rate',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentstohomeworks',
            name='student_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentstohomeworks',
            name='student_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='lesson.student'),
        ),
        migrations.AlterField(
            model_name='studentstohomeworks',
            name='teacher_comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
