from fastapi import APIRouter, Depends
from requests import Session
from app.config.exceptions.business_rule import BusinessRuleException
from app.config.utils.current_user import get_current_user
from app.config.utils.section import get_section
from app.models.user import User
from app.repositories.user.delete_account import delete_account

router = APIRouter()


@router.delete("/me")
async def delete_me(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_section),
):
    user = await delete_account(session, current_user.id)

    if not user:
        raise BusinessRuleException("Error on delete account")

    return {"detail": "Successfully deleted"}
