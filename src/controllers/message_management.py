from fastapi import Query, Path, APIRouter, Depends, Response, status, HTTPException
from fastapi.encoders import jsonable_encoder
from src.models.schema.user import UserResponse, UserRequest, UserRequestUpdatable
from src.models.schema.message import UserMessageRequest, UserMessageResponse, MessagePaginateResponse, MessageResponse
from src.models.data.tracker import User
from src.database.connector import get_db
from src.repository.user import UserRepository
from src.services.message import MessageService
from src.repository.message import MessageRepository
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/message",
    tags=["Messaging system"],
    responses={404: {"description": "Not found"}},
)

@router.post("", status_code=status.HTTP_202_ACCEPTED, response_model=UserMessageResponse)
async def send_message(request: UserMessageRequest, db: Session = Depends(get_db)):
    """
        Submit	a	message	to	a	defined	recipient,	identified	with	some	identifier,	
        e.g.	email-address,	phone-number,	user	name	or	similar. In this case, use e-mail!
    """
    msgService: MessageService = MessageService(db)
    return msgService.send_message(request)

"""
@router.get('/', status_code=status.HTTP_202_ACCEPTED, response_model=MessagePaginateResponse)
async def fetch_all_messages(page: Tuple[SortDirection,int, int] = Depends(pagination.page_size), 
    db: Session = Depends(get_db)):
    msgService: MessageService = MessageService(db)
    resp = msgService.fetch_all_messages(page)
    return resp
"""
@router.get('', status_code=status.HTTP_200_OK, response_model=MessagePaginateResponse)
async def fetch_all_messages(resp: MessagePaginateResponse=Depends(MessageService.fetch_all_msgs_static)):
    """
        Fetch messages (including	previously	fetched) ordered	by	time,	according	
        to	start	and	stop	index.
    """
    return resp

@router.get('/new', status_code=status.HTTP_200_OK, response_model=List[MessageResponse])
async def fetch_new_messages(resp: List[MessageResponse]=Depends(MessageService.fetch_new_msgs_static)):
    """
        Fetch	new messages (meaning	the	service	must	know	what	has	already	
        been	fetched).
    """
    return resp

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_single_message(id: int = Path(1, ge=1), db: Session = Depends(get_db)):
    """
        Delete	a	single	message.
    """
    msgRepository: MessageRepository = MessageRepository(db)
    msgRepository.delete_message_by_id(id=id)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_multiple_messages(
    ids: str = Query(
        default=None, 
        max_length=100, 
        regex="[(\d+)(,)]+\d$",
        description="ids should be a succession of comma separated integers eg. ids=3,4,5,100"
        ), 
    db: Session = Depends(get_db)):
    """
        Delete multiple messages.
    """
    msgService: MessageService = MessageService(db)
    msgService.delete_multiple_msg_by_id(ids)