from django.core.management.base import BaseCommand
from tasks.models import TaskStatus


class Command(BaseCommand):
    help = 'Создает стандартные статусы задач'

    def handle(self, *args, **kwargs):
        statuses = [
            {'id': 0, 'name': 'Новая'},            
            {'id': 1, 'name': 'В процессе'},
            {'id': 2, 'name': 'Завершено'}
        ]

        for status_data in statuses:
            # Используем create() и явно указываем ID, если его нет
            status, created = TaskStatus.objects.get_or_create(
                id=status_data['id'], 
                defaults={'name': status_data['name']}
                )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Статус "{status.name}" с ID {status.id} успешно создан.'))
            else:
                self.stdout.write(self.style.WARNING(f'Статус с ID {status.id} уже существует.'))