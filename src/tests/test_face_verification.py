import pytest
from pytest_mock import MockerFixture
from app.face_verification import FaceVerification

@pytest.mark.parametrize('user_id, file_name', [
    pytest.param(1, 'img_path.jpg', id='is correct'),
    pytest.param(1, '', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param(1, 'img', id='is not correct', marks=pytest.mark.xfail())
])
def test_embeddings_vec(user_id: int, file_name, mocker: MockerFixture):
    vector = mocker.patch('app.face_verification.DeepFace.represent', return_value=[{'embedding': [1,2,3,4,5,6]}])
    mock_db = mocker.Mock()
    mock_user_face_data = mocker.Mock()
    mock_user_face_data.vector = [{'embedding': [1,2,3,4,5,6]}]
    mock_db.query().filter_by().first.return_value = mock_user_face_data
    face_verification = FaceVerification(db=mock_db)
    assert face_verification.verify(user_id, file_name) == True
    vector.assert_called_once()
