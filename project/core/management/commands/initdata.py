import os

import django.core.management
import django.core.management.base
import django.db
import django.db.migrations.executor


class Command(django.core.management.base.BaseCommand):
    help = (
        "Checking database migration plan. "
        "Loads data from a JSON file. "
        "Create a new admin user "
        "with a password from an environment variable"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-checking-database",
            action="store_true",
            help="Add it to skip checking database migrations",
        )

        parser.add_argument(
            "--skip-loading-data",
            action="store_true",
            help="Add it to skip loading data from fixtures to database",
        )

        parser.add_argument(
            "--skip-creating-superuser",
            action="store_true",
            help="Add it to skip creating super user",
        )

        parser.add_argument(
            "--interactive",
            action="store_true",
            help="Add it to create super user interactively"
            ". Fields in .env will not be accepted in that case",
        )

    def handle(self, *args, **options):
        if not options["skip_checking_database"]:
            if not self.check_database():
                return False

        if not options["skip_loading_data"]:
            self.load_data()

        if not options["skip_creating_superuser"]:
            self.create_super_user(options)

    @staticmethod
    def _is_database_synchronized(database):
        connection = django.db.connections[database]
        connection.prepare_database()
        executor = django.db.migrations.executor.MigrationExecutor(connection)
        targets = executor.loader.graph.leaf_nodes()
        return not executor.migration_plan(targets)

    def check_database(self):
        while not self._is_database_synchronized(django.db.DEFAULT_DB_ALIAS):
            self.stdout.write(
                self.style.ERROR("We found not added migrations.")
            )

            self.stdout.write("Do you want to run migration?")
            choice_migrating = input("Type `yes` to continue or `exit`: ")

            if choice_migrating.lower() in ("yes", "да"):
                django.core.management.call_command("migrate")
            else:
                return False

        self.stdout.write(
            self.style.SUCCESS("All migrations have been applied")
        )
        return True

    @staticmethod
    def load_data():
        django.core.management.call_command("loaddata", "fixture.json")

    def _check_superuser_env(self):
        extra_fields = {}

        checkers = {
            "username": "DJANGO_SUPERUSER_USERNAME",
            "email": "DJANGO_SUPERUSER_EMAIL",
            "password": "DJANGO_SUPERUSER_PASSWORD",
        }
        for name, env_name in checkers.items():
            if not os.environ.get(env_name):
                self.stdout.write(
                    self.style.ERROR(f"{env_name} not found in .env")
                )
                extra_fields[name] = input(f"Enter {name}: ")

        return extra_fields

    def create_super_user(self, options):
        interactive = options["interactive"]

        if interactive:
            django.core.management.call_command(
                "createsuperuser", interactive=True
            )

        else:
            extra_fields = self._check_superuser_env()

            try:
                django.core.management.call_command(
                    "createsuperuser", **extra_fields, interactive=False
                )
            except django.core.management.base.CommandError as e:
                self.stdout.write(self.style.ERROR(e))

                self.stdout.write(
                    "Do you want to create superuser interactively?"
                )
                choice_superuser = input("Type `yes` to continue or `exit`: ")

                if choice_superuser.lower() in ("yes", "да"):
                    django.core.management.call_command(
                        "createsuperuser", interactive=True
                    )
