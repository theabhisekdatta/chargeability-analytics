import pytest

from mcp_client import call_mcp_tool
from agent.graph_builder import build_graph


@pytest.fixture(scope="session")
def graph():
    """
    Build the LangGraph only once for all tests.
    """
    return build_graph()


@pytest.fixture(scope="session")
def mcp():
    """
    Returns the MCP client function.
    """
    return call_mcp_tool