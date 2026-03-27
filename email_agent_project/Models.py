from typing import Literal

from pydantic import BaseModel, Field


class EmailDraftInput(BaseModel):
	recipient_name: str = Field(description="받는 사람 이름")
	recipient_email: str = Field(description="받는 사람 이메일")
	sender_name: str = Field(description="보내는 사람 이름")
	purpose: str = Field(description="이메일의 목적")
	key_points: list[str] = Field(default_factory=list, description="본문에 반영할 핵심 포인트 목록")
	tone: Literal["formal", "neutral", "friendly"] = Field(
		default="formal",
		description="이메일 톤"
	)
	language: Literal["ko", "en"] = Field(default="ko", description="이메일 언어")


class EmailDraft(BaseModel):
	draft_id: str = Field(description="초안 고유 ID")
	subject: str = Field(description="이메일 제목")
	body: str = Field(description="이메일 본문")
	tone: str = Field(description="이메일 톤")
	language: str = Field(description="이메일 언어")
	recipient_name: str = Field(description="받는 사람 이름")
	recipient_email: str = Field(description="받는 사람 이메일")
	sender_name: str = Field(description="보내는 사람 이름")
	purpose: str = Field(description="이메일 목적")
	key_points: list[str] = Field(default_factory=list, description="핵심 포인트 목록")
	status: Literal["draft", "sent"] = Field(default="draft", description="초안 상태")
	revised_from: str | None = Field(default=None, description="수정 전 초안 ID")


class ToneRecommendation(BaseModel):
	recommended_tone: Literal["formal", "neutral", "friendly"] = Field(description="추천 톤")
	reason: str = Field(description="추천 사유")


class DraftSendResult(BaseModel):
	draft_id: str = Field(description="발송한 초안 ID")
	recipient_email: str = Field(description="수신자 이메일")
	status: Literal["sent"] = Field(default="sent", description="발송 상태")


