import chainlit as cl
from src.main import app


@cl.on_chat_start
async def start():
    await cl.Message(content="**Astra Fin Pro** is ready. \nAsk me about stocks, news, or internal memos.").send()


@cl.on_message
async def main(message: cl.Message):
    # Initialize the container for the final answer
    msg = cl.Message(content="")

    # Pass user input to the graph
    inputs = {
        "question": message.content,
        "messages": [message.content],
        "revision_count": 0
    }

    try:
        async for output in app.astream(inputs):
            for node_name, value in output.items():

                if node_name == "analyst" and "messages" in value:
                    last_msg = value["messages"][-1]

                    content = last_msg.content if hasattr(last_msg, "content") else str(last_msg)

                    await msg.stream_token(content)

    except Exception as e:
        await msg.stream_token(f"Error: {str(e)}")

    await msg.update()