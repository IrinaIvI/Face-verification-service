import pytest
import json
from aiokafka import AIOKafkaConsumer
from unittest.mock import AsyncMock, MagicMock
from app.consumer import Consumer
import logging

@pytest.fixture
def mock_kafka_consumer(mocker):
    """Фикстура для мока Kafka Consumer."""
    mock_consumer = mocker.patch('consumer.AIOKafkaConsumer')
    mock_consumer.return_value = AsyncMock()
    return mock_consumer

@pytest.fixture
def mock_face_verification(mocker):
    """Фикстура для мока FaceVerification."""
    mock_verification = mocker.patch('app.consumer.FaceVerification')
    mock_verification.return_value.embedings_vector.return_value = [1, 2, 3, 4, 5, 6]
    mock_verification.return_value.check_user.return_value = True
    return mock_verification

@pytest.mark.asyncio
async def test_consumer_process_message_logs(caplog, mock_kafka_consumer, mock_face_verification):
    """Тест для проверки логов при обработке сообщения."""
    # Подготовка данных
    test_message = {
        "photo_path": "test_photo.jpg",
        "user_id": 1
    }

    # Создаем объект Consumer
    consumer = Consumer()

    # Настраиваем mock Kafka consumer, чтобы вернуть наше тестовое сообщение
    mock_kafka_consumer.return_value.__aiter__.return_value = [
        MagicMock(value=json.dumps(test_message).encode('utf-8'))
    ]

    # Запускаем Consumer и обрабатываем сообщение
    with caplog.at_level(logging.INFO):
        await consumer.start()

    # Проверяем, что нужные сообщения были записаны в лог
    assert "Получено сообщение" in caplog.text
    assert "Началась обработка фото" in caplog.text
    assert "Обработка фото завершена" in caplog.text
    assert "Verification result for user" in caplog.text
