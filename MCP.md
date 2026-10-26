# Public read-only MCP

Connect any Streamable HTTP MCP client to `https://gym.sayakanlawannn.my.id/mcp` (no authentication).
Tools: `get_dataset_metadata`, `search_exercises`, `get_exercise`.
Search supports bounded pagination (1–100), name substring, category/equipment/target exact filters. Detail supports dataset languages. No write tools, credentials or user data.

Run `pip install -r requirements.txt`, then `python mcp_server.py` (port 8000). Test: `python test_mcp.py [URL]`.
Deploy `Dockerfile.mcp` separately; static app unchanged from its last deployed custom UI commit `0a9441692063a90343b0cbe7f3c57161c7800494`.

Upstream checked: hasaneyldrm/exercises-dataset `7455efae41b330c265e7cd4b78dfa848e7ce5ebd`. Fork main already matches upstream dataset: 1324 exercises, zero further upstream changes. Dataset retained exactly, including multilingual instructions, media IDs and attribution. Custom UI recovered from last successful deployment because fork main had reverted to upstream. No upstream UI merged. LICENSE and NOTICE.md retained.
