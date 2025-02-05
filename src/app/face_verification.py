from deepface import DeepFace
from app.models import UserFaceData
from datetime import datetime
from sqlalchemy.orm import Session
import logging
logging.basicConfig(level=logging.INFO)


class FaceVerification:
    """Класс обработки фотографии."""

    def __init__(self, db: Session):
        """Инициализация класса верификации."""
        self.db = db

    def embedings_vector(self, img_path: str) -> list[float]:
        """Формирование вектора."""
        vector = DeepFace.represent(img_path=img_path)
        return vector

    def verify(self, user_id: int, img_path: str) -> bool:
        """Верификация пользователя."""
        try:
            vector = self.embedings_vector(img_path=img_path)
        except Exception as verify_error:
            logging.error(f'Ошибка при создании вектора: {verify_error}')
            return False

        verified = self.check_user(user_id, vector)
        return verified

    def check_user(self, user_id: int, vector: list[float]) -> bool:
        """Проверка наличия пользователя в базе."""
        verified = False
        embedding_vector = vector[0].get('embedding')

        try:
            user_face_data = self.db.query(UserFaceData).filter_by(user_id=user_id).first()

            if user_face_data:
                if user_face_data.vector == vector:
                    verified = True
                else:
                    user_face_data.vector = vector
                    user_face_data.updated_at = datetime.now()
                    self.db.commit()
                    verified = True
            else:
                new_user_face_data = UserFaceData(
                    user_id=user_id,
                    vector=embedding_vector,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                self.db.add(new_user_face_data)
                self.db.commit()
                verified = True

        except Exception as error_db:
            logging.error(f'Ошибка при доступе к базе данных: {error_db}')

        return verified
