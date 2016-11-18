from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS


class Command(BaseCommand):
    help = "Quietly change a user's password for django.contrib.auth."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('username', type=str,
            help='Username to change password for.')
        parser.add_argument('password', type=str,
            help='Password (will not be validated).')
        parser.add_argument('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS,
            help='Specifies the database to use. Default is "default".')

    def handle(self, *args, **options):

        username = options['username']
        password = options['password']

        user_model_cls = get_user_model()

        try:
            u = user_model_cls._default_manager \
                    .using(options.get('database')) \
                    .get(**{user_model_cls.USERNAME_FIELD: username})
        except user_model_cls.DoesNotExist:
            raise CommandError("user '%s' does not exist" % username)

        u.set_password(password)
        u.save()

        return "Password changed successfully for user '%s'" % u
