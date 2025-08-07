from django.core.management.base import BaseCommand
from Donotechapp.models import Year, Semester

class Command(BaseCommand):
    help = 'Create Year and Semester instances for years 1 to 4 with their respective semesters'

    def handle(self, *args, **kwargs):
        # Mapping of years to their respective semesters
        year_semester_map = {
            1: [1, 2],
            2: [3, 4],
            3: [5, 6],
            4: [7, 8],
        }

        for year_num, semesters in year_semester_map.items():
            year, created = Year.objects.get_or_create(number=year_num)
            if created:
                self.stdout.write(f'Created Year {year.number}')
            else:
                self.stdout.write(f'Year {year.number} already exists')

            # Print semesters before deletion
            existing_semesters = Semester.objects.filter(year=year)
            self.stdout.write(f'Existing semesters for Year {year.number} before deletion: {[s.number for s in existing_semesters]}')

            # Delete all semesters for this year
            Semester.objects.filter(year=year).delete()

            # Print after deletion
            existing_semesters_after = Semester.objects.filter(year=year)
            self.stdout.write(f'Semesters for Year {year.number} after deletion: {[s.number for s in existing_semesters_after]}')

            for sem_num in semesters:
                semester, created = Semester.objects.get_or_create(year=year, number=sem_num)
                if created:
                    self.stdout.write(f'Created Semester {semester.number} for Year {year.number}')
                else:
                    self.stdout.write(f'Semester {semester.number} for Year {year.number} already exists')
