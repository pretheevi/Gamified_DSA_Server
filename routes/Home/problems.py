from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from security.token_handler import verify_token
from crud_db.crud_problems import Problems
from models.authentication_model import TimePayload

router = APIRouter()

@router.get("/")
async def get_problems(user_data=Depends(verify_token)):
    try:
        user_id = user_data.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token"
            )
        
        problems_data = Problems.get_all_problems(user_id)
        print(problems_data)
        if not problems_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No problems found"
            )
        
        # Transform the data into a more user-friendly format if needed
        formatted_data = [
            {
                "id": problem[0],
                "title": problem[1],
                "slug": problem[2],
                "url": problem[3],
                "topic": problem[4],
                "difficulty": problem[5],
                "xp_value": problem[6],
                "user_problem_progress_id": problem[7],
                "user_id": problem[8],
                "status": problem[9],
                "time_spent": problem[10],
                "last_updated": problem[11]
            } for problem in problems_data
        ]
        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content=formatted_data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )


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
        
        # You can now safely use user_id, problem_id, and payload.time
        # Example logic:
        print(f"User {user_id} spent {payload.time} seconds on problem {problem_id}")
        return {"msg": "Time recorded successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
