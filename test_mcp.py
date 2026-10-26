"""Run: python test_mcp.py [HTTP URL]; defaults to in-process protocol test."""
import asyncio
import sys
from fastmcp import Client
from mcp_server import mcp

async def main():
    async with Client(sys.argv[1] if len(sys.argv) > 1 else mcp) as client:
        tools = await client.list_tools()
        assert {t.name for t in tools} == {'get_dataset_metadata', 'search_exercises', 'get_exercise'}
        metadata = (await client.call_tool('get_dataset_metadata', {})).data
        assert metadata['count'] == 1324
        page = (await client.call_tool('search_exercises', {'query': 'sit-up', 'limit': 1})).data
        assert len(page['exercises']) == 1 and page['total'] > 0
        row = (await client.call_tool('get_exercise', {'exercise_id': page['exercises'][0]['id']})).data
        assert row['name'] == page['exercises'][0]['name'] and row['instructions']
        for args in ({'limit': 101}, {'offset': -1}):
            try:
                await client.call_tool('search_exercises', args)
                raise AssertionError('Invalid pagination accepted')
            except Exception as error:
                assert 'limit must' in str(error)
        print({'tools': sorted(t.name for t in tools), 'count': metadata['count'], 'sample': row['id'], 'validation': 'passed'})

asyncio.run(main())
