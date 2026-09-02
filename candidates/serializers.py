from rest_framework import serializers

from candidates.models import Candidate


class CandidateSerializer(serializers.ModelSerializer):
    """Camel-cased payload consumed by the React Native client."""

    id = serializers.CharField(source="pk", read_only=True)
    rollNumber = serializers.CharField(source="roll_number", read_only=True)
    fatherName = serializers.CharField(source="father_name", read_only=True)
    authorizationNo = serializers.CharField(source="authorization_no", read_only=True)
    testType = serializers.CharField(source="test_type", read_only=True)
    contactNo = serializers.CharField(source="contact_no", read_only=True)
    examCity = serializers.CharField(source="exam_city", read_only=True)
    graduatingCountry = serializers.CharField(
        source="graduating_country", read_only=True
    )
    graduatingCollege = serializers.CharField(
        source="graduating_college", read_only=True
    )
    reportingTime = serializers.CharField(source="reporting_time", read_only=True)
    testTiming = serializers.CharField(source="test_timing", read_only=True)
    examCenter = serializers.CharField(source="exam_center", read_only=True)
    centerLocation = serializers.CharField(source="center_location", read_only=True)
    testMonth = serializers.CharField(source="test_month", read_only=True)

    class Meta:
        model = Candidate
        fields = (
            "id",
            "rollNumber",
            "name",
            "fatherName",
            "authorizationNo",
            "email",
            "testType",
            "contactNo",
            "gender",
            "city",
            "examCity",
            "graduatingCountry",
            "graduatingCollege",
            "session",
            "reportingTime",
            "testTiming",
            "examCenter",
            "centerLocation",
            "testMonth",
            "image",
        )


class CandidateSummarySerializer(CandidateSerializer):
    """Same shape without the heavy base64 image, for list responses."""

    class Meta(CandidateSerializer.Meta):
        fields = tuple(f for f in CandidateSerializer.Meta.fields if f != "image")


class UserDetailsRequestSerializer(serializers.Serializer):
    verificationId = serializers.CharField(max_length=128)
