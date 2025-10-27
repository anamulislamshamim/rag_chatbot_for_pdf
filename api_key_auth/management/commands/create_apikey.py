from django.core.management.base import BaseCommand, CommandError
from api_key_auth.models import APIKey


class Command(BaseCommand):
    help = "Create a new API key. Prints plaintext once."

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Name for the api key')
        parser.add_argument('--notes', type=str, default='', help='Optional notes')
    
    def handle(self, *args, **options):
        name = options['name']
        notes = options['notes']
        obj, plaintext = APIKey.create_key(name=name, notes=notes)
        self.stdout.write("Name: %s" % obj.name)
        self.stdout.write("Plaintext API key (copy and store it now; only shown once):")
        self.stdout.write(plaintext)