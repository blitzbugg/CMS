# Generated migration to rename IsActive to IsActive for Django auth compatibility

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_module', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tblstaff',
            old_name='IsActive',
            new_name='IsActive',
        ),
    ]
