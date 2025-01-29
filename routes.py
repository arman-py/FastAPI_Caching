from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from database import get_session
from models import CachedTransformation, Payload
from schemas import InputData
from utils import compute_hash, transformer_function

router = APIRouter()


@router.post("/payload")
async def create_payload(data: InputData, session: Session = Depends(get_session)):
    payload_id = compute_hash(data.list_1, data.list_2)
    existing_payload = session.exec(
        select(Payload).where(Payload.payload_id == payload_id)
    ).first()
    if existing_payload:
        return {"payload_id": existing_payload.payload_id}

    transformed_list = []
    for text in data.list_1 + data.list_2:
        cached = session.exec(
            select(CachedTransformation).where(CachedTransformation.input_text == text)
        ).first()
        if cached:
            transformed_list.append(cached.output_text)
        else:
            transformed_text = await transformer_function(text)
            session.add(
                CachedTransformation(input_text=text, output_text=transformed_text)
            )
            transformed_list.append(transformed_text)

    interleaved_result = [
        val
        for pair in zip(
            transformed_list[: len(data.list_1)], transformed_list[len(data.list_1) :]
        )
        for val in pair
    ]
    new_payload = Payload(payload_id=payload_id, content=", ".join(interleaved_result))
    session.add(new_payload)
    session.commit()
    return {"payload_id": payload_id}


@router.get("/payload/{payload_id}")
async def read_payload(payload_id: str, session: Session = Depends(get_session)):
    payload = session.exec(
        select(Payload).where(Payload.payload_id == payload_id)
    ).first()
    if not payload:
        raise HTTPException(status_code=404, detail="Payload not found")
    return {"output": payload.content}
