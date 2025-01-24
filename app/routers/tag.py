from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session, selectinload
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import Post, Tag
from app.schemas import CreateTag, UpdateTag, PostResponse
from sqlalchemy import insert, select, update, delete

router = APIRouter(prefix='/tag', tags=['tag'])


@router.get('/tags')
async def all_tags(db: Annotated[Session, Depends(get_db)]):
    tags = db.scalars(select(Tag)).all()
    return tags


@router.post('/create_tag')
async def create_tag(db: Annotated[Session, Depends(get_db)], cr_tag: CreateTag):
    new_tag=Tag(title=cr_tag.title)
    db.add(new_tag)
    """db.scalar(insert(Tag).values(title=cr_tag.title))"""
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Tag created successful!'}


@router.put('/update_tag')
async def update_tag(tag_id: int, db: Annotated[Session, Depends(get_db)], update_tag: UpdateTag):
    tag = db.scalar(select(Tag).where(Tag.id == tag_id))
    if tag is None:
        raise HTTPException(status_code=404, detail='Tag was not found')

    db.execute(update(Tag).where(Tag.id == tag_id).values(title=update_tag.title))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Tag updated successful!'}


@router.get('/tag_id')
async def posts_by_tag(tag_id: int, db: Annotated[Session, Depends(get_db)]):
    tag = db.execute(
        select(Tag)
        .options(selectinload(Tag.posts))
        .where(Tag.id == tag_id)
    ).scalar()

    if not tag:
        raise HTTPException(status_code=404, detail='Tag not found')

    return [PostResponse.model_validate(p) for p in tag.posts]


@router.delete('/delete_tag')
async def delete_post(tag_id: int, db: Annotated[Session, Depends(get_db)]):
    tag = db.scalar(select(Tag).where(Tag.id == tag_id))
    if tag is None:
        raise HTTPException(status_code=404, detail='Tag was not found')
    db.execute(delete(Tag).where(Tag.id == tag_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Tag deleted successfuly!'}
