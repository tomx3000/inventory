from django.core.management.base import BaseCommand, CommandError
# from polls.models import Question as Poll
from inventory.models import Item
class Command(BaseCommand):
    help = 'Get total value of items'

    def add_arguments(self, parser):
        parser.add_argument('item', nargs='+', type=int)

    def handle(self, *args, **options):
        print(options['item'])
        return Item.objects.check_amount()