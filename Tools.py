"""이메일 초안 생성/조회에 사용하는 도구 모듈."""

from uuid import uuid4

from langchain_core.tools import tool

from Models import DraftSendResult, EmailDraft, EmailDraftInput, ToneRecommendation
from mock_db import get_draft, list_drafts, save_draft, save_sent


def _build_subject(purpose: str) -> str:
	return f"[{purpose.strip()}] 관련 문의 드립니다"


def _build_greeting(recipient_name: str, tone: str) -> str:
	if tone == "친근":
		return f"{recipient_name}님 안녕하세요."
	return f"{recipient_name}님께,"


def _build_closing(sender_name: str, tone: str) -> str:
	if tone == "친근":
		return f"감사합니다.\n{sender_name} 드림"
	return f"검토 부탁드립니다.\n{sender_name} 드림"


def _compose_body(request: EmailDraftInput) -> str:
	greeting = _build_greeting(request.recipient_name, request.tone)
	closing = _build_closing(request.sender_name, request.tone)

	point_lines = "\n".join([f"- {point}" for point in request.key_points]) or "- (핵심 내용 미입력)"
	return (
		f"{greeting}\n\n"
		f"{request.purpose} 관련하여 메일드립니다.\n\n"
		f"핵심 내용은 아래와 같습니다.\n{point_lines}\n\n"
		f"추가로 필요한 사항이 있으면 말씀 부탁드립니다.\n\n"
		f"{closing}"
	)


def _call_style_to_tone(style_request: str, current_tone: str) -> str:
	request = style_request.lower()
	if "친근" in style_request or "부드럽" in style_request:
		return "친근"
	if "정중" in style_request or "공손" in style_request or "격식" in style_request or "공식" in style_request:
		return "공식"
	if "중립" in style_request:
		return "중립"
	return current_tone


def _extract_extra_line(style_request: str) -> str | None:
	for marker in ["추가:", "add:"]:
		if marker in style_request:
			line = style_request.split(marker, 1)[1].strip()
			return line if line else None
	return None


@tool
def recommend_email_tone(
	recipient_type: str,
	purpose: str,
	urgency: str = "normal",
) -> dict:
	"""수신자 유형/목적/긴급도 기반으로 이메일 톤을 추천합니다."""
	recipient_hint = recipient_type.strip().lower()
	purpose_hint = purpose.strip().lower()
	urgency_hint = urgency.strip().lower()

	if recipient_hint in {"고객", "customer", "executive", "임원", "상사"}:
		recommended = "공식"
		reason = "수신자가 외부 이해관계자 또는 의사결정권자이므로 격식 있는 톤이 적합합니다."
	elif urgency_hint in {"high", "긴급", "urgent"}:
		recommended = "공식"
		reason = "긴급 커뮤니케이션은 오해를 줄이기 위해 명확하고 정중한 톤이 유리합니다."
	elif any(token in purpose_hint for token in ["감사", "축하", "후기", "thanks", "appreciat"]):
		recommended = "친근"
		reason = "관계 강화 목적이므로 친근한 톤이 효과적입니다."
	else:
		recommended = "중립"
		reason = "일반 업무 커뮤니케이션에 균형 잡힌 중립 톤이 적합합니다."

	return ToneRecommendation(recommended_tone=recommended, reason=reason).model_dump()


@tool
def create_email_draft(
	recipient_name: str,
	recipient_email: str,
	sender_name: str,
	purpose: str,
	key_points: str = "",
	tone: str = "공식",
) -> dict:
	"""이메일 초안을 생성하고 저장합니다.

	Args:
		recipient_name: 받는 사람 이름
		recipient_email: 받는 사람 이메일
		sender_name: 보내는 사람 이름
		purpose: 이메일 목적
		key_points: 반영할 핵심 포인트 문자열(예: "A;B;C")
		tone: 이메일 톤(공식|중립|친근)

	Returns:
		생성된 이메일 초안(dict)
	"""
	points = [point.strip() for point in key_points.split(";") if point.strip()]
	request = EmailDraftInput(
		recipient_name=recipient_name,
		recipient_email=recipient_email,
		sender_name=sender_name,
		purpose=purpose,
		key_points=points,
		tone=tone,
	)

	subject = _build_subject(request.purpose)
	body = _compose_body(request)

	draft = EmailDraft(
		draft_id=str(uuid4()),
		subject=subject,
		body=body,
		tone=request.tone,
		language="ko",
		recipient_name=request.recipient_name,
		recipient_email=request.recipient_email,
		sender_name=request.sender_name,
		purpose=request.purpose,
		key_points=request.key_points,
	).model_dump()

	save_draft(draft)
	return draft


@tool
def get_saved_email_drafts(limit: int = 5) -> list[dict]:
	"""저장된 최근 이메일 초안을 조회합니다."""
	return list_drafts(limit)


@tool
def revise_email_draft(draft_id: str, revision_request: str) -> dict:
	"""기존 초안을 수정 요청에 맞춰 재작성합니다."""
	current = get_draft(draft_id)
	if current is None:
		return {"error": f"draft_id={draft_id} 인 초안을 찾을 수 없습니다."}

	new_tone = _call_style_to_tone(revision_request, current["tone"])
	extra_line = _extract_extra_line(revision_request)

	request = EmailDraftInput(
		recipient_name=current["recipient_name"],
		recipient_email=current["recipient_email"],
		sender_name=current["sender_name"],
		purpose=current["purpose"],
		key_points=current.get("key_points", []),
		tone=new_tone,
	)

	body = _compose_body(request)
	if extra_line:
		body = f"{body}\n\n{extra_line}"

	revised = EmailDraft(
		draft_id=str(uuid4()),
		subject=current["subject"],
		body=body,
		tone=new_tone,
		language="ko",
		recipient_name=current["recipient_name"],
		recipient_email=current["recipient_email"],
		sender_name=current["sender_name"],
		purpose=current["purpose"],
		key_points=current.get("key_points", []),
		revised_from=current["draft_id"],
	).model_dump()

	save_draft(revised)
	return revised


@tool
def send_email_draft(draft_id: str) -> dict:
	"""초안을 발송 처리합니다(현재는 모의 발송)."""
	draft = get_draft(draft_id)
	if draft is None:
		return {"error": f"draft_id={draft_id} 인 초안을 찾을 수 없습니다."}

	draft["status"] = "sent"
	result = DraftSendResult(
		draft_id=draft["draft_id"],
		recipient_email=draft["recipient_email"],
	).model_dump()
	save_sent(result)
	return result
