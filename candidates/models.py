from django.db import models


class Candidate(models.Model):
    """One examinee row imported from the exam-centre spreadsheet."""

    serial = models.PositiveIntegerField(db_index=True)
    roll_number = models.CharField(max_length=16, unique=True, db_index=True)
    name = models.CharField(max_length=120)
    father_name = models.CharField(max_length=120, blank=True)
    authorization_no = models.CharField(max_length=32, blank=True)
    email = models.CharField(max_length=254, blank=True)
    test_type = models.CharField(max_length=64, blank=True)
    contact_no = models.CharField(max_length=32, blank=True)
    gender = models.CharField(max_length=16, blank=True)
    city = models.CharField(max_length=64, blank=True)
    exam_city = models.CharField(max_length=64, blank=True)
    graduating_country = models.CharField(max_length=64, blank=True)
    graduating_college = models.CharField(max_length=200, blank=True)
    session = models.CharField(max_length=32, blank=True)
    reporting_time = models.CharField(max_length=32, blank=True)
    test_timing = models.CharField(max_length=32, blank=True)
    exam_center = models.CharField(max_length=300, blank=True)
    center_location = models.URLField(max_length=500, blank=True)
    test_month = models.CharField(max_length=32, blank=True)

    # Base64-encoded PNG (no data: prefix) — sample data until real photos land.
    image = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["serial"]

    def __str__(self) -> str:
        return f"{self.roll_number} - {self.name}"


class VerificationAttempt(models.Model):
    """Audit row written when the app fetches details after an SDK run."""

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="verification_attempts",
    )
    verification_id = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.candidate.roll_number} @ {self.created_at:%Y-%m-%d %H:%M:%S}"
