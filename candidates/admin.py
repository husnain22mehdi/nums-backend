from django.contrib import admin
from django.utils.html import format_html

from candidates.models import Candidate, VerificationAttempt


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("serial", "roll_number", "name", "gender", "city", "test_type")
    search_fields = ("roll_number", "name", "father_name", "city")
    list_filter = ("gender", "test_type", "graduating_country", "session")
    readonly_fields = ("photo", "created_at", "updated_at")

    @admin.display(description="Photo")
    def photo(self, obj: Candidate) -> str:
        if not obj.image:
            return "-"
        return format_html(
            '<img src="data:image/png;base64,{}" width="96" height="96" />',
            obj.image,
        )


@admin.register(VerificationAttempt)
class VerificationAttemptAdmin(admin.ModelAdmin):
    list_display = ("candidate", "verification_id", "created_at")
    search_fields = ("candidate__roll_number", "verification_id")
