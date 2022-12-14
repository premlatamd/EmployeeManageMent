# Generated by Django 4.1.3 on 2022-12-06 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendence',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('In_Time', models.TimeField(null=True)),
                ('Out_Time', models.TimeField(null=True)),
                ('Work_type', models.CharField(max_length=50, null=True)),
                ('Salary', models.CharField(max_length=50)),
                ('duration', models.DurationField(null=True)),
                ('total_second', models.FloatField(null=True)),
                ('sub_total', models.DecimalField(decimal_places=2, max_digits=300, null=True)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PayementStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('stu_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=6, max_digits=300, null=True)),
                ('receiver', models.CharField(max_length=50, null=True)),
                ('completed_salary', models.DecimalField(decimal_places=2, max_digits=300, null=True)),
                ('due_salary', models.DecimalField(decimal_places=2, max_digits=300, null=True)),
                ('attend_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.attendence')),
                ('emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.usermodel')),
            ],
        ),
        migrations.AddField(
            model_name='attendence',
            name='emp_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.usermodel'),
        ),
        migrations.AlterUniqueTogether(
            name='attendence',
            unique_together={('emp_id', 'date')},
        ),
    ]
