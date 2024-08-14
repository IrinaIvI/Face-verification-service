from deepface import DeepFace
from dataclasses import dataclass, field
from aiokafka import AIOKafkaConsumer
import asyncio
import os
import logging


KAFKA_BROKER = os.environ.get('KAFKA_BROKER', 'localhost:9092')
KAFKA_TOPIC = 'face_verification'
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
                self.process_message(message)
        finally:
            await self.consumer.stop()

    def process_message(self, message):
        """Обработка сообщения из Kafka."""
        logging.info(f"Получено сообщение: {message.value.decode()}")

@dataclass
class User:
    """Класс создание пользователя."""

    id: int
    verified: bool = False
    vector: list[float] = field(default_factory=list[float])


class UserStorage:
    """Класс хранилища с пользователями."""

    storage: dict[str, User] = {}

    def add_user(self, user: User):
        """Добавление пользователя в базу."""
        UserStorage().storage['FaceNet'] = user

    def get_user(self, user_id: int) -> User:
        """Получение пользователя по айди."""
        for model, user in UserStorage().storage.items():
            if model == FaceVerification.model:
                if user.id == user_id:
                    return user

    def update_user(self, user: User) -> User:
        """Обновление существующего пользователя."""
        for model, current_user in UserStorage().storage.items():
            if model == FaceVerification.model:
                if current_user.id == user.id:
                    current_user = user
                    return current_user


class FaceVerification:
    """Класс обработки фотографии."""

    user_storage: UserStorage = UserStorage()
    model: str = 'FaceNet'

    def verify(self, user_id: int, img_path: str) -> bool:
        """Верификация пользователя."""
        vector = DeepFace.represent(img_path=img_path)
        return self.check_user(user_id, vector)

    def check_user(self, user_id: int, vector: list[float]) -> bool:
        """Проверка наличия пользователя в базе."""
        verified = False
        user = self.user_storage.get_user(user_id)
        if user:
            if user.vector == vector:
                verified = True
            else:
                verified = True
                updated_user = User(user_id, verified, vector)
                self.user_storage.update_user(updated_user)
        else:
            verified = True
            new_user = User(user_id, verified, vector)
            self.user_storage.add_user(new_user)
        return verified
