from deepface import DeepFace
from app.models import UserFaceData
from datetime import datetime
from sqlalchemy.orm import Session
import logging
logging.basicConfig(level=logging.INFO)

class FaceVerification:
    """Класс обработки фотографии."""

    def __init__(self, db: Session):
        self.db = db

    def verify(self, user_id: int, img_path: str) -> bool:
        """Верификация пользователя."""
        logging.info("Верификация начата")

        try:
            vector = DeepFace.represent(img_path=img_path)
            logging.info("Вектор создан: %s", vector)
        except Exception as e:
            logging.error("Ошибка при создании вектора: %s", e)
            return False

        try:
            verified = self.check_user(user_id, vector)
        except Exception as e:
            logging.error("Ошибка при проверке пользователя: %s", e)
            return False

        return verified

    def check_user(self, user_id: int, vector: list[float]) -> bool:
        """Проверка наличия пользователя в базе."""
        logging.info("Проверка пользователя с ID %d", user_id)
        verified = False
        embedding_vector = vector[0].get('embedding')

        try:
            user_face_data = self.db.query(UserFaceData).filter_by(user_id=user_id).first()

            if user_face_data:
                if user_face_data.vector == vector:
                    logging.info("Пользователь найден и вектор совпадает")
                    verified = True
                else:
                    logging.info("Пользователь найден, но вектор обновлён")
                    user_face_data.vector = vector
                    user_face_data.updated_at = datetime.now()
                    self.db.commit()
                    verified = True
            else:
                logging.info("Пользователь не найден, добавление новой записи")
                new_user_face_data = UserFaceData(
                    user_id=user_id,
                    vector=embedding_vector,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                self.db.add(new_user_face_data)
                self.db.commit()
                verified = True

        except Exception as e:
            logging.error("Ошибка при доступе к базе данных: %s", e)

        return verified
