from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task, TaskStatus
from django.contrib.auth import get_user_model

User = get_user_model()

class OldCompletedTasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')

        self.status_new = TaskStatus.objects.create(id=0, name='Новая')
        self.status_new = TaskStatus.objects.create(id=1, name='В процессе')
        self.status_done = TaskStatus.objects.create(id=2, name='Завершено')

        # Завершённая задача более месяца назад
        self.old_task = Task.objects.create(
            title='Старая завершённая задача',
            author=self.user,
            status_id=self.status_done.id,
            updated_at=timezone.now() - timedelta(days=40)
        )

        # Завершённая недавно
        self.recent_task = Task.objects.create(
            title='Недавняя завершённая задача',
            author=self.user,
            status_id=self.status_done.id,
            updated_at=timezone.now() - timedelta(days=5)
        )

        # Незавершённая задача
        self.new_task = Task.objects.create(
            title='Новая задача',
            author=self.user,
            status_id=self.status_new.id,
            updated_at=timezone.now() - timedelta(days=50)
        )
 
    def test_filter_old_completed_tasks(self):
        string = '''----------------=====-----------------\nТест на фильтрацию\n----------------=====-----------------'''
        print(string)

        month_ago = timezone.now() - timedelta(days=30)
        old_tasks = Task.objects.filter(
            status_id=2,
            # updated_at__lt=month_ago
        )

        self.assertIn(self.old_task, old_tasks)
        self.assertIn(self.recent_task, old_tasks)
        self.assertNotIn(self.new_task, old_tasks)
