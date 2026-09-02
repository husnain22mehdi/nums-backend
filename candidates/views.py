import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from candidates.models import Candidate, VerificationAttempt
from candidates.serializers import (
    CandidateSerializer,
    CandidateSummarySerializer,
    UserDetailsRequestSerializer,
)

logger = logging.getLogger(__name__)


@api_view(["GET"])
def check_roll_number(_request: Request, roll_number: str) -> Response:
    """GET /api/users/<roll_number>/exists -> {"exists": bool}"""
    exists = Candidate.objects.filter(roll_number=roll_number).exists()
    return Response({"exists": exists})


@api_view(["POST"])
def user_details(request: Request, roll_number: str) -> Response:
    """POST /api/users/<roll_number>/details -> {"user": {...}}

    Called only after the native SDK reports a successful verification, so the
    verification id is required and recorded.
    """
    payload = UserDetailsRequestSerializer(data=request.data)
    payload.is_valid(raise_exception=True)

    try:
        candidate = Candidate.objects.get(roll_number=roll_number)
    except Candidate.DoesNotExist:
        return Response(
            {"code": "USER_NOT_FOUND", "message": "Roll number not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    VerificationAttempt.objects.create(
        candidate=candidate,
        verification_id=payload.validated_data["verificationId"],
    )
    logger.info(
        "Verified candidate %s with verification id %s",
        candidate.roll_number,
        payload.validated_data["verificationId"],
    )

    return Response({"user": CandidateSerializer(candidate).data})


@api_view(["GET"])
def candidate_list(_request: Request) -> Response:
    """GET /api/users -> {"users": [...]} — convenience endpoint for debugging."""
    candidates = Candidate.objects.all()
    return Response({"users": CandidateSummarySerializer(candidates, many=True).data})


@api_view(["GET"])
def health(_request: Request) -> Response:
    return Response({"status": "ok", "candidates": Candidate.objects.count()})
