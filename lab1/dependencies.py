from fastapi import Depends, Request
from typing import Annotated

def get_text_id_from_cookie(request: Request):
    text_id_cookie = request.cookies.get("current_text_id")
    return int(text_id_cookie) if text_id_cookie else None

TextIdDep = Annotated[int|None, Depends(get_text_id_from_cookie)]