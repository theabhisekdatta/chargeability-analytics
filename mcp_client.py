import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"


async def _call_tool(
    tool_name: str,
    question: str
) -> str:

    async with streamable_http_client(
        MCP_SERVER_URL
    ) as (
        read_stream,
        write_stream,
        _
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            # Initialize MCP connection
            await session.initialize()

            # Call MCP tool
            result = await session.call_tool(
                tool_name,
                {
                    "question": question
                }
            )

            # Extract text response
            responses = []

            for content in result.content:

                if hasattr(content, "text"):
                    responses.append(content.text)

                else:
                    responses.append(str(content))

            return "\n".join(responses)


def call_mcp_tool(
    tool_name: str,
    question: str
) -> str:

    return asyncio.run(
        _call_tool(
            tool_name,
            question
        )
    )