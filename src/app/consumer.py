from aiokafka import AIOKafkaConsumer
import logging
import os
import json
from app.face_verification import FaceVerification
from app.database import get_db

KAFKA_BROKER = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
KAFKA_TOPIC = 'ivashko_topic_face_verification'
logging.basicConfig(level=logging.INFO)

class Consumer:
    """Класс для прослушивания топика Kafka и обработки сообщений."""

    def __init__(self):
        self.consumer = AIOKafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_BROKER)

    async def start(self):
        """Запускает консумер и обрабатывает сообщения."""
        await self.consumer.start()
        try:
            async for message in self.consumer:
                await self.process_message(message)
        finally:
            await self.consumer.stop()

    async def process_message(self, message):
        """Обработка сообщения из Kafka."""
        decoded_message = message.value.decode('utf-8')
        logging.info(f"Получено сообщение: {decoded_message}")

        data = json.loads(decoded_message)
        img_path = data.get('photo_path')
        user_id = data.get('user_id')

        logging.info(f'Извлечённые данные - img_path: {img_path}, user_id: {user_id}')

        if img_path and user_id:
            db = next(get_db())
            face_verification = FaceVerification(db)
            verified = face_verification.verify(user_id, img_path)
            logging.info(verified)

