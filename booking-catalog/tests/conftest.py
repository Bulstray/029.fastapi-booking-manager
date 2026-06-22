from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
from httpx2 import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)


@pytest.fixture(scope="module", autouse=True)
async def create_db():
    from core.config import settings

    settings.db.url = "sqlite+aiosqlite:///:memory:"

    from core.models import Base, db_helper

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="module")
async def client() -> AsyncGenerator[AsyncClient]:
    from main import app

    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test/api/v1/bookings",
    ) as test_client:
        yield test_client


@pytest.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession]:
    from core.models import db_helper

    async with db_helper.session_factory() as connection:
        yield connection


@pytest.fixture(scope="function")
def mock_taskiq():
    with patch(
        "api.api_v1.booking.update_service_type.kiq",
        new_callable=AsyncMock,
    ) as mock:
        yield mock
