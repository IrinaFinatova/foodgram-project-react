from django.db import migrations

INITIAL_TAGS = [{'color': '#20B2AA', 'name': 'Завтрак', 'slug': 'breakfast'},
                {'color': '#FF00FF', 'name': 'Обед', 'slug': 'dinner'},
                {'color': '#008000', 'name': 'Ужин', 'slug': 'supper'}]


def add_tags(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    for tag in INITIAL_TAGS:
        new_tag = Tag(**tag)
        new_tag.save()


def remove_tags(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    for tag in INITIAL_TAGS:
        Tag.objects.get(slug=tag['slug']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(add_tags, remove_tags)
    ]
