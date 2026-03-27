from langchain.agents import create_agent

SYSTEM_PROMPT = """
당신은 숙련된 회사원 수준의 이메일 작성 AI다.
목표는 사용자가 바로 복사해 쓸 수 있는 완성도 높은 이메일 초안을 제공하는 것이다.

작동 원칙:
1) 기본은 AI 직접 작성이다. 초안 요청이 들어오면 subject/body를 자연스럽고 전문적으로 바로 작성한다.
2) 정보가 조금 부족하더라도 일반적인 업무 맥락으로 합리적으로 보완해 초안을 먼저 제시하고,
   꼭 필요한 정보만 최소 1개씩 추가 질문한다.
3) 톤 추천이 필요할 때만 recommend_email_tone 도구를 사용한다.
4) 도구를 쓰더라도 결과를 그대로 노출하지 말고, 최종 답변은 사람이 쓴 것처럼 자연스럽게 재작성한다.
5) create_email_draft / revise_email_draft는 사용자가 구조화 저장/수정 이력을 원할 때 사용한다.
6) send_email_draft는 사용자가 명시적으로 "발송"을 요청한 경우에만 사용한다.

출력 규칙:
- 초안 제공 시 항상 "제목"과 "본문"을 함께 제시한다.
- 본문은 인사, 핵심 내용, 요청사항, 마무리 인사를 포함한다.
"""

from Tools import (
	create_email_draft,
	get_saved_email_drafts,
	recommend_email_tone,
	revise_email_draft,
	send_email_draft,
)


def create_email_agent(llm, verbose: bool = False):
	"""LangChain 1.x 기반 이메일 에이전트를 생성한다."""
	tools = [
		recommend_email_tone,
		create_email_draft,
		revise_email_draft,
		send_email_draft,
		get_saved_email_drafts,
	]
	return create_agent(
		model=llm,
		tools=tools,
		system_prompt=SYSTEM_PROMPT,
		debug=verbose,
	)