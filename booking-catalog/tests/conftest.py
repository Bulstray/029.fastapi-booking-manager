from collections.abc import AsyncGenerator, Generator
from unittest.mock import AsyncMock, patch

import pytest
from httpx2 import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from core.models import Base, db_helper


@pytest.fixture(scope="module", autouse=True)
async def create_db() -> None:
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


@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession]:

    async with db_helper.session_factory() as connection:
        yield connection


@pytest.fixture
def mock_taskiq() -> Generator[AsyncMock]:
    with patch(
        "api.api_v1.booking.update_service_type.kiq",
        new_callable=AsyncMock,
    ) as mock:
        yield mock
