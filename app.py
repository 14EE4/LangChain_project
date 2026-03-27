from dotenv import load_dotenv
from langchain_groq import ChatGroq

from agent import create_email_agent

load_dotenv()

def run_demo() -> None:
    groq_llm_model = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.3,
    )
    agent = create_email_agent(llm=groq_llm_model, verbose=False)

    print("이메일 에이전트 시작. 종료하려면 exit 입력")
    messages = []

    while True:
        try:
            user_input = input("you> ").strip()
        except EOFError:
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "q"}:
            print("종료합니다.")
            break

        messages.append({"role": "user", "content": user_input})
        response = agent.invoke({"messages": messages})
        assistant_message = response["messages"][-1].content
        print(f"agent> {assistant_message}")

        # tool call 히스토리를 포함해 다음 턴 문맥으로 사용한다.
        messages = response["messages"]


if __name__ == "__main__":
    run_demo()
