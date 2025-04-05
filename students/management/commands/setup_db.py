from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from students.models import Department

class Command(BaseCommand):
    help = 'Sets up initial database with superuser and departments'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))

        # Create departments if they don't exist
        departments = [
            'Computer Science',
            'Information Technology',
            'Electronics and Communication',
            'Electrical Engineering',
            'Mechanical Engineering',
            'Civil Engineering'
        ]

        for dept in departments:
            Department.objects.get_or_create(name=dept)
        
        self.stdout.write(self.style.SUCCESS('Departments created successfully'))
