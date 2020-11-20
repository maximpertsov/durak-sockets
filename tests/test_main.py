import pytest

from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_status():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
