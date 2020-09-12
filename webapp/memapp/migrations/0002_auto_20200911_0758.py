# Generated by Django 3.1 on 2020-09-11 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='member_details',
            fields=[
                ('detail_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=50)),
                ('phone_num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='member_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_number', models.IntegerField(default=0)),
                ('member_name', models.CharField(max_length=100)),
                ('notes', models.CharField(max_length=250)),
                ('dob', models.DateField()),
                ('is_committee', models.BooleanField(default=False)),
                ('pronouns', models.CharField(max_length=25)),
                ('join_date', models.DateField()),
            ],
        ),
        migrations.DeleteModel(
            name='member_exception',
        ),
        migrations.DeleteModel(
            name='membership',
        ),
        migrations.AddField(
            model_name='member_details',
            name='id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='memapp.member_info'),
        ),
    ]
