from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = ['managers']
MODELS = ['article', 'comment', 'bloguser', 'tag', 'topic']
PERMISSIONS = ['view', 'add', 'change']


class Command(BaseCommand):
	help = 'Creates read only default permission groups for users'

	def handle(self, *args, **options):
		for group in GROUPS:
			new_group, _ = Group.objects.get_or_create(name=group)
			for model in MODELS:
				for permission in PERMISSIONS:
					codename = '{}_{}'.format(permission, model)
					print("Creating {}".format(codename))

					model_add_perm = Permission.objects.get(codename=codename)
					new_group.permissions.add(model_add_perm)

		print("Created default group and permissions.")
