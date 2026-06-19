from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("emissions", "0006_add_total_source_validation"),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadAudit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=512, null=True, blank=True)),
                ('idempotency_key', models.CharField(max_length=128, null=True, blank=True, db_index=True)),
                ('file_hash', models.CharField(max_length=128, null=True, blank=True, db_index=True)),
                ('created_count', models.IntegerField(default=0)),
                ('updated_count', models.IntegerField(default=0)),
                ('failed_count', models.IntegerField(default=0)),
                ('skipped_count', models.IntegerField(default=0)),
                ('processing_status', models.CharField(default='pending', max_length=32, choices=[('pending','pending'),('processing','processing'),('completed','completed'),('failed','failed')])),
                ('error_message', models.TextField(null=True, blank=True)),
                ('started_at', models.DateTimeField(null=True, blank=True)),
                ('finished_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
            ],
        ),
    ]
