from django.db.utils import IntegrityError
from django.db import migrations, transaction

from ..utils import get_invite_code


def create_users(apps, schema_editor):
    User = apps.get_model('core', 'User')
    for i in range(3):
        try:
            with transaction.atomic():
                User.objects.create(phone_number=f'+7922822277{i}', username=f'user{i}', invite_code=get_invite_code())
        except IntegrityError:
            continue
    referrer = User.objects.get(pk=1)
    User.objects.filter(pk__gt=1).update(is_ref=True, referrer=referrer)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_users)]
