import json
from pathlib import Path
from fastmcp import FastMCP

DATA = json.loads((Path(__file__).parent / "data/exercises.json").read_text())
mcp = FastMCP("Gym Exercise Dataset")

@mcp.tool

def get_dataset_metadata() -> dict:
    """Get count, filter values, languages and upstream attribution."""
    return {"count": len(DATA), "upstream": "https://github.com/hasaneyldrm/exercises-dataset", "license": "See https://github.com/rizkidarmawan21/exercises-dataset/blob/main/NOTICE.md and LICENSE", "filters": {k: sorted({str(x.get(k, '')) for x in DATA}) for k in ('category', 'equipment', 'target')}, "languages": sorted(DATA[0]['instructions'])}

@mcp.tool

def search_exercises(query: str = '', category: str = '', equipment: str = '', target: str = '', offset: int = 0, limit: int = 20) -> dict:
    """Search names, exact case-insensitive filters; summaries only. Fetch detail by ID."""
    if not 1 <= limit <= 100 or not 0 <= offset <= len(DATA):
        raise ValueError('limit must be 1..100; offset must be 0..dataset count')
    if any(len(v) > 200 for v in (query, category, equipment, target)):
        raise ValueError('Search strings must be at most 200 characters')
    rows = [x for x in DATA if query.casefold() in x['name'].casefold() and all(not v or str(x.get(k, '')).casefold() == v.casefold() for k, v in [('category', category), ('equipment', equipment), ('target', target)])]
    return {'total': len(rows), 'offset': offset, 'limit': limit, 'has_more': offset + limit < len(rows), 'exercises': [{k: x.get(k) for k in ('id', 'name', 'category', 'equipment', 'target')} for x in rows[offset:offset+limit]]}

@mcp.tool

def get_exercise(exercise_id: str, language: str = 'en') -> dict:
    """Get one exercise, localized instructions and source attribution. IDs retain leading zeros."""
    if len(exercise_id) > 32 or len(language) > 10:
        raise ValueError('Invalid ID or language')
    row = next((x for x in DATA if x['id'] == exercise_id), None)
    if row is None:
        raise ValueError('Exercise not found')
    if language not in row['instructions']:
        raise ValueError('Unsupported language')
    result = dict(row)
    for field in ('instructions', 'instruction_steps'):
        result[field] = row[field][language]
    return result

if __name__ == '__main__':
    # ponytail: immutable in-memory dataset; use indexed storage only if it outgrows RAM.
    mcp.run(transport='http', host='0.0.0.0', port=8000, stateless_http=True)
