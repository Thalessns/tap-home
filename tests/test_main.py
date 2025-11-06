"""Tests for main application lifespan and configuration."""

import pytest

from httpx import ASGITransport, AsyncClient
from unittest.mock import AsyncMock

from src.app import main
from src.app.main import app
from tests.conftest import app_url


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_main(monkeypatch):
    """Test the lifespan of the FastAPI application."""

    mock_init = AsyncMock()
    monkeypatch.setattr(main, "lifespan", mock_init)
    async with AsyncClient(transport=ASGITransport(app=app), base_url=app_url) as client:
        response = await client.get("/")

        mock_init.ass
        assert response.status_code == 200
        assert response.json() == {"message": "API is running"}
        assert app.title == "Python API Crud"
        assert app.version == "0.1.0"
        assert any("/tag" in route.path for route in app.routes)
