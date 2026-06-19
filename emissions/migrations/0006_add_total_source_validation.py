from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("emissions", "0005_remove_carbonemission_emissions_c_industr_d36899_idx_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name='carbonemission',
            name='total_emission',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='carbonemission',
            name='source',
            field=models.CharField(choices=[('manual', 'manual'), ('bulk', 'bulk'), ('sensor', 'sensor'), ('predicted', 'predicted')], default='manual', max_length=32),
        ),
        migrations.AddField(
            model_name='carbonemission',
            name='validation_status',
            field=models.CharField(choices=[('valid', 'valid'), ('pending', 'pending'), ('invalid', 'invalid')], default='valid', max_length=32),
        ),
        migrations.AddIndex(
            model_name='carbonemission',
            index=models.Index(fields=['date'], name='emissions_date_idx'),
        ),
        migrations.AddIndex(
            model_name='carbonemission',
            index=models.Index(fields=['industry', 'date'], name='emissions_industry_date_idx'),
        ),
    ]
