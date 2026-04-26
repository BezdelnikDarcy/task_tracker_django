from django.core.management.base import BaseCommand
from pathlib import Path
from django.core.files import File
from config import settings
from task_manager.models import Attachments

class Command(BaseCommand):
    def handle(self, *args, **options):
        path = Path(settings.MEDIA_ROOT) / "external_images" / "some_file_text.txt"

        at = Attachments.objects.get(id=5)
        with path.open('rb') as f:
            at.file = File(f, name=path.name)
            at.save()