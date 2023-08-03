# Generated by Django 3.2.20 on 2023-07-17 17:59

from django.db import migrations, models
import django.db.models.deletion
import libs.mixins
import libs.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('hostname', models.CharField(max_length=50)),
                ('port', models.IntegerField(null=True)),
                ('username', models.CharField(max_length=50)),
                ('pkey', models.TextField(null=True)),
                ('desc', models.CharField(max_length=255, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.CharField(default=libs.utils.human_datetime, max_length=20)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='account.user')),
            ],
            options={
                'db_table': 'hosts',
                'ordering': ('-id',),
            },
            bases=(models.Model, libs.mixins.ModelMixin),
        ),
        migrations.CreateModel(
            name='HostExtend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance_id', models.CharField(max_length=64, null=True)),
                ('zone_id', models.CharField(max_length=30, null=True)),
                ('cpu', models.IntegerField()),
                ('memory', models.FloatField()),
                ('disk', models.CharField(default='[]', max_length=255)),
                ('os_name', models.CharField(max_length=50)),
                ('os_type', models.CharField(max_length=20)),
                ('private_ip_address', models.CharField(max_length=255)),
                ('public_ip_address', models.CharField(max_length=255)),
                ('instance_charge_type', models.CharField(choices=[('PrePaid', '包年包月'), ('PostPaid', '按量计费'), ('Other', '其他')], max_length=20)),
                ('internet_charge_type', models.CharField(choices=[('PayByTraffic', '按流量计费'), ('PayByBandwidth', '按带宽计费'), ('Other', '其他')], max_length=20)),
                ('created_time', models.CharField(max_length=20, null=True)),
                ('expired_time', models.CharField(max_length=20, null=True)),
                ('updated_at', models.CharField(default=libs.utils.human_datetime, max_length=20)),
                ('host', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='host.host')),
            ],
            options={
                'db_table': 'host_extend',
            },
            bases=(models.Model, libs.mixins.ModelMixin),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('parent_id', models.IntegerField(default=0)),
                ('sort_id', models.IntegerField(default=0)),
                ('hosts', models.ManyToManyField(related_name='groups', to='host.Host')),
            ],
            options={
                'db_table': 'host_groups',
                'ordering': ('-sort_id',),
            },
            bases=(models.Model, libs.mixins.ModelMixin),
        ),
    ]