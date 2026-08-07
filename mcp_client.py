import asyncio
import os

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


# Local:
#   MCP_SERVER_URL=http://127.0.0.1:8000/mcp
#
# Docker:
#   MCP_SERVER_URL=http://mcp-server:8000/mcp

MCP_SERVER_URL = os.getenv(
    "MCP_SERVER_URL",
    "http://127.0.0.1:8000/mcp",
)


def _call_local_tool(tool_name: str, question: str) -> str:
    from mcp_server import ask_documents as ask_local, generate_sql as generate_sql_local

    if tool_name == "ask_documents":
        return ask_local(question)
    if tool_name == "generate_sql":
        return generate_sql_local(question)
    raise ValueError(f"Unsupported local tool: {tool_name}")


async def _call_tool(
    tool_name: str,
    question: str,
) -> str:
    """
    Calls an MCP tool and returns the response as plain text.
    """

    try:
        async with streamable_http_client(
            MCP_SERVER_URL
        ) as (
            read_stream,
            write_stream,
            _,
        ):

            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:

                await session.initialize()

                result = await session.call_tool(
                    tool_name,
                    {"question": question},
                )

                responses = []

                for content in result.content:
                    if hasattr(content, "text"):
                        responses.append(content.text)
                    else:
                        responses.append(str(content))

                return "\n".join(responses)

    except Exception:
        try:
            return _call_local_tool(tool_name, question)
        except Exception as local_exc:
            return f"MCP Error: {local_exc}"


def call_mcp_tool(
    tool_name: str,
    question: str,
) -> str:
    """
    Synchronous wrapper around the async MCP client.
    """

    return asyncio.run(
        _call_tool(
            tool_name=tool_name,
            question=question,
        )
    )


if __name__ == "__main__":

    print(
        call_mcp_tool(
            "ask_documents",
            "What is Generating Labor Cost?",
        )
    )