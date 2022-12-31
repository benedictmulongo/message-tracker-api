from fastapi import Query, status, HTTPException, Depends
from typing import Union, Optional, List, Tuple
from sqlalchemy.orm import Session
from enum import Enum

class SortDirection(str, Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"

# Use creator model design pattern ? for diff. dependencies
class Pagination:
    # Should depends on the number of messages in database
    def __init__(self, maximum_limit: int = 100):
        self.maximum_limit = maximum_limit

    async def start_end_limit(self,start: int = Query(0, ge=0), end: int = Query(10, ge=0)) -> Tuple[int, int]:
        return (start, end)

    async def page_size_computed(self,page_number: int = Query(1, ge=1),page_size: int = Query(10, ge=0)) -> Tuple[int, int]:
        page_size = min(self.maximum_limit, page_size)
        start = int(page_number - 1) * page_size
        end = start + page_size
        return (start, end)

    async def page_size(self, sortDir: Optional[SortDirection]=SortDirection.ASCENDING, page_number: int = Query(1, ge=1),page_size: int = Query(10, ge=0)) -> Tuple[int, int]:
        page_size = min(self.maximum_limit, page_size)
        return (sortDir, page_number, page_size)


    def get_date(msg):
        # messages.sort(key=get_date, reverse=True)
        # return messages[page[0]:page[1]]
        return msg.send_date