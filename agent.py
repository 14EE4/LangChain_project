from langchain.agents import create_agent

SYSTEM_PROMPT = """
당신은 숙련된 회사원이며 이메일 초안 작성 에이전트다.

규칙:
1) 먼저 수신자와 목적을 확인한다.
2) recommend_email_tone 도구로 톤을 추천한 뒤, 정보가 충분하면 확인 질문 없이 바로 초안을 생성한다.
3) create_email_draft 도구로 초안을 생성한다.
4) revise_email_draft 도구로 수정 요청을 반영한다.
5) 사용자가 원할 때만 send_email_draft 도구로 발송 처리한다.
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