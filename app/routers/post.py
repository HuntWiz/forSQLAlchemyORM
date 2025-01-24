from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session, selectinload
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import Post, Tag
from app.schemas import CreatePost, UpdatePost
from sqlalchemy import insert, select, update, delete
from app.schemas import PostResponse

from slugify import slugify

router = APIRouter(prefix='/post', tags=['post'])

@router.get('/posts')
async def all_posts(db:Annotated[Session, Depends(get_db)]):
    posts = db.scalars(select(Post)).all()
    return posts

@router.get('/post_id')
async def user_by_id(post_id:int, db: Annotated[Session, Depends(get_db)]):
    post = db.scalar(select(Post).where(Post.id == post_id))
    if post is not None:
        return post
    else:
        raise HTTPException(status_code=404, detail='Post was not found')


@router.post('/create_post')
async def create_post(db:Annotated[Session, Depends(get_db)], create_post: CreatePost):
    db.execute(insert(Post).values(title=create_post.title,
                                   content=create_post.content,
                                   ))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put('/update_post')
async def update_post(post_id:int, db:Annotated[Session, Depends(get_db)], update_post: UpdatePost):
    post = db.scalar(select(Post).where(Post.id == post_id))
    if post is None:
        raise HTTPException(status_code=404, detail='User was not found')

    db.execute(update(Post).where(Post.id == post_id).values(title=update_post.title,
                                   content=update_post.content,
                                   ))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Post updated successful!'}

@router.get('/{tag_id}/posts', response_model=list[PostResponse])
async def posts_by_tag(tag_id: int, db: Annotated[Session, Depends(get_db)]):
    tag = db.execute(
        select(Tag)
        .options(selectinload(Tag.posts))
        .where(Tag.id == tag_id)
    ).scalar()

    if not tag:
        raise HTTPException(status_code=404, detail='Tag not found')

    return [PostResponse.model_validate(p) for p in tag.posts]

@router.delete('/delete_post')
async def delete_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = db.scalar(select(Post).where(Post.id == post_id))
    if post is None:
        raise HTTPException(status_code=404, detail='Post was not found')
    db.execute(delete(Post).where(Post.id == post_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Post deleted successfuly!'}
