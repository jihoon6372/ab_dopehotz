# Generated by Django 2.0 on 2017-12-12 08:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20171212_1444'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=512, null=True)),
                ('user_agent', models.CharField(max_length=255, null=True)),
                ('auth_date', models.DateTimeField(auto_now_add=True, verbose_name='접속일')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='로그인 계정')),
            ],
            options={
                'verbose_name_plural': '로그인 기록',
            },
        ),
    ]
