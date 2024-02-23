from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='photos',
            field=models.FileField(blank=True, null=True, upload_to='photos_services'),
        ),
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons_categories'),
        ),
        migrations.AlterField(
            model_name='service',
            name='cep',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='service',
            name='city',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='service',
            name='date',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='service',
            name='hours_service',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='service',
            name='neighbor',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='service',
            name='number',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='service',
            name='rating',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='service',
            name='state',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='service',
            name='status',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='service',
            name='street',
            field=models.CharField(max_length=255),
        ),
    ]
