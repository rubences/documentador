import pytest

from app.estimation.messaging.redis_job_store import RedisJobStore
from app.shared.schemas import EstimationResponse


class _FakeRedis:
    def __init__(self) -> None:
        self.data: dict[str, str] = {}

    async def ping(self) -> bool:
        return True

    async def aclose(self) -> None:
        return None

    async def get(self, key: str):
        return self.data.get(key)

    async def set(self, key: str, value: str) -> None:
        self.data[key] = value


@pytest.mark.asyncio
async def test_redis_job_store_lifecycle_and_status_flow(monkeypatch) -> None:
    fake_redis = _FakeRedis()
    monkeypatch.setattr(
        "app.estimation.messaging.redis_job_store.Redis.from_url",
        lambda *_args, **_kwargs: fake_redis,
    )

    store = RedisJobStore(redis_url="redis://fake:6379/0", key_prefix="test:job")
    await store.connect()

    await store.create_pending(job_id="job-1", correlation_id="corr-1")
    queued = await store.get("job-1")
    assert queued is not None
    assert queued["status"] == "queued"
    assert queued["progress"] == 0

    await store.set_processing("job-1")
    processing = await store.get("job-1")
    assert processing is not None
    assert processing["status"] == "processing"
    assert processing["progress"] == 50

    result = EstimationResponse(
        estimation="## Estimacion\n\n- Horas: 100\n- Coste: 6250 EUR",
        model="mock-model",
        provider="mock-provider",
        usage={"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
    )
    await store.set_completed("job-1", result)
    completed = await store.get("job-1")
    assert completed is not None
    assert completed["status"] == "completed"
    assert completed["progress"] == 100
    assert completed["result"]["provider"] == "mock-provider"

    await store.close()


@pytest.mark.asyncio
async def test_redis_job_store_failure_state(monkeypatch) -> None:
    fake_redis = _FakeRedis()
    monkeypatch.setattr(
        "app.estimation.messaging.redis_job_store.Redis.from_url",
        lambda *_args, **_kwargs: fake_redis,
    )

    store = RedisJobStore(redis_url="redis://fake:6379/0", key_prefix="test:job")
    await store.connect()

    await store.create_pending(job_id="job-2", correlation_id="corr-2")
    await store.set_failed("job-2", "simulated failure")

    failed = await store.get("job-2")
    assert failed is not None
    assert failed["status"] == "failed"
    assert failed["progress"] == 100
    assert failed["error"] == "simulated failure"

    await store.close()
