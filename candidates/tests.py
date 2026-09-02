import base64
import json

from django.test import TestCase
from django.urls import reverse

from candidates.management.commands.import_candidates import (
    build_sample_avatar,
    clean,
    initials_of,
)
from candidates.models import Candidate, VerificationAttempt


class CandidateFactory:
    @staticmethod
    def create(**overrides) -> Candidate:
        defaults = {
            "serial": 1,
            "roll_number": "91086798",
            "name": "Waqas Yasin",
            "father_name": "Muhammad Yasin",
            "exam_center": "King Hamad University of Nursing, Islamabad",
            "image": build_sample_avatar("Waqas Yasin", 1),
        }
        defaults.update(overrides)
        return Candidate.objects.create(**defaults)


class CheckRollNumberTests(TestCase):
    def setUp(self) -> None:
        self.candidate = CandidateFactory.create()

    def test_existing_roll_number(self) -> None:
        response = self.client.get(
            reverse("check-roll-number", args=[self.candidate.roll_number])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"exists": True})

    def test_unknown_roll_number(self) -> None:
        response = self.client.get(reverse("check-roll-number", args=["99999999"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"exists": False})


class UserDetailsTests(TestCase):
    def setUp(self) -> None:
        self.candidate = CandidateFactory.create()
        self.url = reverse("user-details", args=[self.candidate.roll_number])

    def post(self, payload: dict) -> "TestCase.client.response_class":
        return self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )

    def test_returns_camel_cased_candidate(self) -> None:
        response = self.post({"verificationId": "ver-1"})

        self.assertEqual(response.status_code, 200)
        user = response.json()["user"]
        self.assertEqual(user["rollNumber"], "91086798")
        self.assertEqual(user["name"], "Waqas Yasin")
        self.assertEqual(user["fatherName"], "Muhammad Yasin")
        self.assertTrue(user["image"].startswith("iVBORw0KGgo"))

    def test_records_the_verification_attempt(self) -> None:
        self.post({"verificationId": "ver-1"})

        attempt = VerificationAttempt.objects.get()
        self.assertEqual(attempt.candidate, self.candidate)
        self.assertEqual(attempt.verification_id, "ver-1")

    def test_rejects_a_missing_verification_id(self) -> None:
        response = self.post({})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(VerificationAttempt.objects.count(), 0)

    def test_unknown_roll_number_returns_404(self) -> None:
        response = self.client.post(
            reverse("user-details", args=["99999999"]),
            data=json.dumps({"verificationId": "ver-1"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["code"], "USER_NOT_FOUND")


class ImporterHelperTests(TestCase):
    def test_initials(self) -> None:
        self.assertEqual(initials_of("Waqas Yasin"), "WY")
        self.assertEqual(initials_of("Cher"), "CH")
        self.assertEqual(initials_of("   "), "?")

    def test_clean_formats_dates_and_whole_floats(self) -> None:
        import datetime as dt

        self.assertEqual(clean(dt.date(2026, 5, 1)), "May 2026")
        self.assertEqual(clean(8141.0), "8141")
        self.assertEqual(clean("  spaced  "), "spaced")
        self.assertEqual(clean(None), "")

    def test_sample_avatar_is_a_png(self) -> None:
        encoded = build_sample_avatar("Arisha Arif", 3)
        self.assertEqual(base64.b64decode(encoded)[:8], b"\x89PNG\r\n\x1a\n")
