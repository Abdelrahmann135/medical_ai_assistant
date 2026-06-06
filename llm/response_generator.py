from langchain_core.runnables.history import RunnableWithMessageHistory
from llm.memory import get_session_history
from app.resources import llm


def run_chain(prompt, variables, user_id="user_1"):

    chain = prompt | llm()

    chain_with_memory = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="query",
        history_messages_key="history"
    )

    response = chain_with_memory.invoke(
        variables,
        config={
            "configurable": {
                "session_id": user_id
            }
        }
    )

    return response.content