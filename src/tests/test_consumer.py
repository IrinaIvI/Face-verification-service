import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from app.consumer import Consumer
import logging

@pytest.fixture
def mock_kafka_consumer(mocker):
    """Фикстура для мока Kafka Consumer."""
    mock_consumer = mocker.patch('app.consumer.AIOKafkaConsumer')
    mock_consumer.return_value = AsyncMock()
    return mock_consumer

@pytest.fixture
def mock_face_verification(mocker):
    """Фикстура для мока FaceVerification."""
    mock_verification = mocker.patch('app.consumer.FaceVerification')
    mock_verification_instance = mock_verification.return_value
    mock_verification_instance.verify = MagicMock(return_value=True)
    return mock_verification_instance

@pytest.mark.asyncio
async def test_consumer_process_message_logs(caplog, mock_kafka_consumer, mock_face_verification):
    """Тест для проверки логов при обработке сообщения."""
    test_message = {
        "photo_path": "test_photo.jpg",
        "user_id": 1
    }
    consumer = Consumer()
    mock_kafka_consumer.return_value.__aiter__.return_value = [
        AsyncMock(value=json.dumps(test_message).encode('utf-8'))
    ]
    with caplog.at_level(logging.INFO):
        await consumer.start()
    assert "Получено сообщение" in caplog.text
    assert "Извлечённые данные - img_path: test_photo.jpg, user_id: 1" in caplog.text
    mock_face_verification.verify.assert_called_once_with(1, "test_photo.jpg")
