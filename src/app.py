import chainlit as cl
from src.graph.astra_graph import build_graph

# Build the graph once
graph = build_graph()


@cl.on_chat_start
async def start():
    await cl.Message(
        content="**👋 Astra Fin Pro is ready.**\n\nTry asking: *'I have 50k INR and want high risk.'*").send()


@cl.on_message
async def main(message: cl.Message):
    # Initialize the stream container
    final_answer = cl.Message(content="")

    # 1. Show the "Thinking" Loader
    async with cl.Step(name="Astra Brain", type="run") as step:
        step.input = message.content

        inputs = {"query": message.content}

        # 2. Stream the Graph Events
        async for chunk in graph.astream(inputs, stream_mode="updates"):
            for node, values in chunk.items():

                # VISUALIZE: The Planner (Brain)
                if node == "planner":
                    intent = values.get("intent", "unknown")
                    await cl.Message(
                        author="🧠 Brain",
                        content=f"Identified Intent: **{intent.upper()}**",
                        parent_id=message.id
                    ).send()

                # VISUALIZE: The Memory (Profile)
                elif node == "investor_profile":
                    if values.get("profile_updated"):
                        p = values.get("investor_profile", {})
                        details = f"Budget: {p.get('budget')} {p.get('currency')} | Risk: {p.get('risk')}"
                        await cl.Message(
                            author="📝 Memory",
                            content=f"**Profile Updated:**\n{details}",
                            parent_id=message.id
                        ).send()

                # VISUALIZE: The Advisor (Stream Response)
                elif node == "advisor":
                    # Stream the final answer chunks
                    response = values.get("answer", "")
                    await final_answer.stream_token(response)

                # VISUALIZE: Finance Agent / Reasoner
                elif node in ["finance_agent", "reasoner"]:
                    response = values.get("answer", "")
                    await final_answer.stream_token(response)

    # 3. Final Send
    await final_answer.send()