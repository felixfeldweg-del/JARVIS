from livekit.agents import function_tool, RunContext, JobContext
import logging, asyncio

@function_tool
async def shutdown_agent(ctx: RunContext) -> str:
    """Stops the currrent JARVIS session (Standby)"""
    try:
        await asyncio.sleep(3)
        ctx.session.shutdown()
        logging.info("Session stopped on User request")
        return "Shutting down Session"

    except Exception as e:
        logging.info("shuting down session failed")
        return "Shutting down Session failed"

def create_shutdown_tool(job: JobContext):

    @function_tool
    async def shutdown_job(ctx: RunContext) -> str:
        """Stops the LiveKit Job """
        try:
            await asyncio.sleep(3)
            job.shutdown()
            logging.info("Shutting down on User request")
            return "Shutting down Job"

        except Exception as e:
            logging.info("shuting down job failed")
            return "Shutting down Job failed"
    return shutdown_job