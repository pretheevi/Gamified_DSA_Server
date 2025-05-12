from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from security.token_handler import verify_token
from crud_db.crud_problems import Problems
from models.authentication_model import TimePayload, StatusCheck

router = APIRouter()


@router.post('/{problem_id}')
def update_status(
    problem_id: int,
    status: StatusCheck,
    user_data=Depends(verify_token)
):
    try:
        user_id = user_data.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        if not problem_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Problem ID is not mentioned"
            )
        
        if status.status != "Solved":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status is not solved"
            )

        result = Problems.update_status_solved(user_id, problem_id, status.status)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update try again."
            )
        
        return {'msg': 'Status is updated to solved'}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )