from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent, ChatMessage, room_io, ChatContext
from livekit.plugins import (
    google,
    ai_coustics,
)
from SERVER.old.Mem0Client import Mem0Client
from SERVER.old.prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
import json, logging
import os

from tools.LiveKit_tools import shutdown_agent, create_shutdown_tool

load_dotenv(".env")

class Assistant(Agent):
    def __init__(self, chat_ctx=None,shutdown_tool=None) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google.beta.realtime.RealtimeModel(
                temperature=0.7
            ),
            tools=[
                shutdown_agent,
                shutdown_tool
            ],
            chat_ctx=chat_ctx,
            )

server = AgentServer()


@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: agents.JobContext):

    shutdown_tool = create_shutdown_tool(ctx)

    async def shutdown_hook(chat_ctx: ChatContext, mem0: Mem0Client, user_id: str, memory_str: str):
        logging.info("Shutting down, saving chat context")

        messages_formatted = [

        ]
        for item in chat_ctx.items:
            if not isinstance(item, ChatMessage):
                continue

            content_str = "".join(item.content) if isinstance(item.content, list) else str(item.content)
            if memory_str and memory_str in content_str:
                continue
            
            

            if item.role in ["assistant", "user"]:
                messages_formatted.append({
                    "role": item.role,
                    "content": content_str.strip(),
                })
        await mem0.add(user_id=user_id, messages=messages_formatted)
        logging.info("Saved chat context")

    

    session = AgentSession(
        
    )

    mem0_url = os.environ["MEM0_URL"]
    mem0 = Mem0Client(mem0_url)
    user_name = "felix"

    result = await mem0.get_all(user_name)
    inital_ctx= ChatContext()
    memory_str = ""

    if result:
        memories = [
        {
            "memory": result["memory"],
            "updated_at": result["updated_at"],
        }
        for result in result
        ]
        memory_str = json.dumps(memories)
        logging.info(memory_str)
        inital_ctx.add_message(
            role="assistant",
            content=f"Following is a list of relevant memories about the user {user_name} : {memory_str}"
        )

    await session.start(
        room=ctx.room,
        agent=Assistant(chat_ctx=inital_ctx,shutdown_tool=shutdown_tool),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                
                noise_cancellation=ai_coustics.audio_enhancement(model=ai_coustics.EnhancerModel.QUAIL_VF_S),
            ),
            video_input=True,
        ),
    )

    await ctx.connect()
    
    await session.generate_reply(
        instructions=SESSION_INSTRUCTION
    )

    ctx.add_shutdown_callback(lambda: shutdown_hook(session._agent.chat_ctx, mem0, user_name, memory_str))

if __name__ == "__main__":
    agents.cli.run_app(server)

