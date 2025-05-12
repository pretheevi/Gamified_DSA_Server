from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from security.token_handler import verify_token
from crud_db.crud_problems import Problems
from models.authentication_model import TimePayload, StatusCheck

router = APIRouter()

@router.post("/{problem_id}")
def update_time(
    problem_id: int,
    payload: TimePayload,
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

        result = Problems.check_problem_row_already_exists(user_id, problem_id)
        print(result)
        if payload.status == "Solved" and not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Problem not started yet, can't mark it as Solved"
            )

        if payload.status == "Solved" and result:
            Problems.update_time_spend(user_id, problem_id, "Solved", payload.time)
        elif payload.status != "Solved" and not result:
            Problems.insert_new_problem_progress_row(user_id, problem_id, payload.time)
        elif payload.status != "Solved" and result:
            Problems.update_time_spend(user_id, problem_id, payload.status, payload.time)
        print("timer has updated")
        return {"msg": "Time recorded successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )