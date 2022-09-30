import csv
import codecs
from io import BytesIO
from typing import Any, Union
from collections import namedtuple
from fastapi import APIRouter, Request, Depends, HTTPException, Body
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import Response


from app.api import deps
from app.models import User


router = APIRouter(prefix="/users")


@router.get("/{user_id}")
async def get_user(*, db: AsyncSession = Depends(deps.get_db), user_id: int) -> Any:
    sql = text('SELECT id, email, description FROM users WHERE id=:user_id LIMIT 1;')
    result = await db.execute(sql, {'user_id': user_id})
    user = result.fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}


@router.put("")
@router.put("/")
@router.put("/{user_id}")
async def put_user(request: Request, db: AsyncSession = Depends(deps.get_db), user_id: Union[int, None] = None, user: User = Body(User, embed=True)) -> Any:
    payload = await request.json()
    try:
        user = User.validate(payload).modelToDict()
        user.update({"user_id": user_id})
    except Exception as err:
        print(f"endpoints.users.put_user user validate error: {err}")
        raise HTTPException(status_code=500, detail="User data is not valid.")

    if user_id is None:
        sql = '''
            INSERT INTO users (email, description) VALUES (:email, :description)
            ON CONFLICT ON constraint users_email_key DO UPDATE SET description=:description
            RETURNING *;
        '''
        del user["id"]
        del user["user_id"]
    else:
        sql = text('SELECT id, email, description FROM users WHERE id=:user_id LIMIT 1;')
        result = await db.execute(sql, {'user_id': user_id})
        testUser = result.fetchone()
        if testUser is not None:
            sql = "UPDATE users SET email=:email, description=:description WHERE id=:user_id RETURNING *;"
        else:
            sql = "INSERT INTO users (id, email, description) VALUES (:user_id, :email, :description) RETURNING *;"

    result = await db.execute(text(sql), user)
    row = result.fetchone()

    if row is None:
        raise HTTPException(status_code=500, detail="User can't update")

    Record = namedtuple('Record', result.keys())
    updated_user = Record(*row)._asdict()
    await db.commit()

    return updated_user


@router.delete("/{user_id}")
async def delete_user(*, db: AsyncSession = Depends(deps.get_db), user_id: int) -> Any:
    print("delete user user_id: ", user_id)
    sql = text('SELECT id, email, description FROM users WHERE id=:user_id LIMIT 1;')
    result = await db.execute(sql, {'user_id': user_id})
    user = result.fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    sql = text('DELETE FROM users WHERE id=:user_id;')
    await db.execute(sql, {'user_id': user_id})
    await db.commit()
    return {"user_id": user_id, "success": True}


@router.get("")
@router.get("/")
async def get_users(*, db: AsyncSession = Depends(deps.get_db)) -> Response:
    result = await db.execute(text("SELECT * FROM users"))
    fieldnames = [key for key in result.keys()]
    users = result.all()
    Record = namedtuple('Record', result.keys())
    raw_users = [Record(*user)._asdict() for user in users]

    StreamWriter = codecs.getwriter('utf-8')
    file = StreamWriter(BytesIO())
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(raw_users)
    response = Response(file.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=all_users.csv"

    return response
