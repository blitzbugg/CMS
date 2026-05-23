from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import identify_hasher

from apps.admin_module.models import TblStaff


class Command(BaseCommand):
    help = "Re-hash any TblStaff passwords that were accidentally stored in plain text."

    def handle(self, *args, **options):
        updated = 0
        skipped = 0

        for staff in TblStaff.objects.all():
            raw = staff.password or ""
            if not raw:
                skipped += 1
                continue

            try:
                identify_hasher(raw)
                skipped += 1
                continue
            except Exception:
                # Not a valid encoded password -> treat as raw plaintext.
                staff.set_password(raw)
                staff.save(update_fields=["password"])
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Rehashed: {updated} | Skipped: {skipped}"))

