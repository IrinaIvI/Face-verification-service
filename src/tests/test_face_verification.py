from app.face_verification import FaceVerification
import pytest
from pytest_mock import MockerFixture
from app.database import get_db


@pytest.mark.parametrize('user_id, file_name', [
    pytest.param(1, 'img_path.jpg', id='is correct'),
    pytest.param(1, '', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param(1, 'img', id='is not correct', marks=pytest.mark.xfail())
])
def test_embeddings_vec(user_id: int, file_name, mocker: MockerFixture):
    vector = mocker.patch('app.face_verification.DeepFace.represent', return_value = [1,2,3,4,5,6])
    db = next(get_db())
    assert FaceVerification(db).verify(user_id, file_name) == True
    vector.assert_called_once()
