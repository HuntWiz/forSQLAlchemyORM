from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import selectinload
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import Tag
from app.schemas import CreateTag, UpdateTag, PostResponse
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import  AsyncSession

router = APIRouter(prefix='/tag', tags=['tag'])


@router.get('/tags')
async def all_tags(db: Annotated[AsyncSession, Depends(get_db)]):
    tags = await db.execute(select(Tag))
    tags = tags.scalars().all()
    return tags


@router.post('/create_tag')
async def create_tag(db: Annotated[AsyncSession, Depends(get_db)], cr_tag: CreateTag):
    new_tag=Tag(title=cr_tag.title)
    db.add(new_tag)
    """db.scalar(insert(Tag).values(title=cr_tag.title))"""
    await db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Tag created successful!'}


@router.put('/update_tag')
async def update_tag(tag_id: int, db: Annotated[AsyncSession, Depends(get_db)], update_tag: UpdateTag):
    tag = await db.scalar(select(Tag).where(Tag.id == tag_id))
    if tag is None:
        raise HTTPException(status_code=404, detail='Tag was not found')

    await db.execute(update(Tag).where(Tag.id == tag_id).values(title=update_tag.title))
    await db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Tag updated successful!'}


@router.get('/tag_id')
async def posts_by_tag(tag_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    tag =await db.execute(
        select(Tag)
        .options(selectinload(Tag.posts))
        .where(Tag.id == tag_id))

    tag = tag.scalar()

    if not tag:
        raise HTTPException(status_code=404, detail='Tag not found')

    return [PostResponse.model_validate(p) for p in tag.posts]


@router.delete('/delete_tag')
async def delete_tag(tag_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    tag = await db.scalar(select(Tag).where(Tag.id == tag_id))
    if tag is None:
        raise HTTPException(status_code=404, detail='Tag was not found')
    await db.execute(delete(Tag).where(Tag.id == tag_id))
    await db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Tag deleted successfuly!'}
