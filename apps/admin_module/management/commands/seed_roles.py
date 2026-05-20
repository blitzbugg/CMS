from django.core.management.base import BaseCommand
from apps.admin_module.models import TblRole
from apps.receptionist.models import TblMembership

class Command(BaseCommand):
    help = 'Seeds default roles and membership types'

    def handle(self, *args, **options):
        # Seed Roles
        roles = ['Administrator', 'Receptionist', 'Doctor', 'Pharmacist', 'Lab Technician']
        for role_name in roles:
            role, created = TblRole.objects.get_or_create(RoleName=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Role '{role_name}' created successfully."))
            else:
                self.stdout.write(f"Role '{role_name}' already exists.")

        # Seed Memberships
        memberships = ['General', 'Premium', 'VIP']
        for membership_name in memberships:
            membership, created = TblMembership.objects.get_or_create(MembershipName=membership_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Membership '{membership_name}' created successfully."))
            else:
                self.stdout.write(f"Membership '{membership_name}' already exists.")
