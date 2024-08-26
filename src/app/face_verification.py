from deepface import DeepFace
from app.models import UserFaceData
from datetime import datetime
class FaceVerification:
    """Класс обработки фотографии."""


    def verify(self, user_id: int, img_path: str) -> bool:
        """Верификация пользователя."""
        vector = DeepFace.represent(img_path=img_path)
        return self.check_user(user_id, vector)

    def check_user(self, user_id: int, vector: list[float]) -> bool:
        """Проверка наличия пользователя в базе."""
        verified = False
        user_face_data = self.db_session.query(UserFaceData).filter_by(user_id=user_id).first()
        if user_face_data:
            if user_face_data.vector == vector:
                verified = True
            else:
                user_face_data.vector = vector
                user_face_data.updated_at = datetime.now()
                self.db_session.commit()
                verified = True
        else:
            new_user_face_data = UserFaceData(
                user_id=user_id,
                vector=vector,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self.db_session.add(new_user_face_data)
            self.db_session.commit()
            verified = True

        return verified
