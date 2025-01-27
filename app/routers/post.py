from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session, selectinload
from app.backend.db_depends import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Post, Tag
from app.schemas import CreatePost, UpdatePost, PostGetTagsModel
from sqlalchemy import insert, select, update, delete
from app.schemas import PostResponse


router = APIRouter(prefix='/post', tags=['post'])

@router.get('/posts')
async def all_posts(db:Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Post))
    posts = result.scalars().all()
    return posts

@router.get('/post_id/{post_id}')
async def post_by_id(post_id:int, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await db.scalar(select(Post).where(Post.id == post_id))
    if post is not None:
        return post
    else:
        raise HTTPException(status_code=404, detail='Post was not found')


@router.post('/create_post')
async def create_post(db:Annotated[AsyncSession, Depends(get_db)], create_post: CreatePost):
    result = await db.execute(insert(Post).values(title=create_post.title,
                                   content=create_post.content,
                                   ).returning(Post.id))
    await db.commit()
    post_id = result.scalar()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful',
            'id': post_id}

@router.post('/{post_id}/get_tags')
async def post_get_tags(post_id: int, db:Annotated[AsyncSession, Depends(get_db)], posts_tags: PostGetTagsModel):
    post = await db.scalar(select(Post).where(Post.id == post_id))
    if post is None:
        raise HTTPException(status_code=404, detail='Post was not found')

    tags = await db.execute(select(Tag).filter(Tag.id.in_(posts_tags.tags_id)))
    tags = tags.scalars().all()
    post.tags.extend(tags)
    await db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': f"Добавлено {len(tags)} тегов к посту {post_id}"}

@router.put('/update_post/{post_id}')
async def update_post(post_id:int, db:Annotated[AsyncSession, Depends(get_db)], update_post: UpdatePost):
    post = await db.scalar(select(Post).where(Post.id == post_id))
    if post is None:
        raise HTTPException(status_code=404, detail='Post was not found')

    await db.execute(update(Post).where(Post.id == post_id).values(title=update_post.title,
                                   content=update_post.content,
                                   ))
    await db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Post updated successful!'}

@router.get('/{tag_id}/posts', response_model=list[PostResponse])
async def posts_by_tag(tag_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    tag = await db.execute(
        select(Tag)
        .options(selectinload(Tag.posts))
        .where(Tag.id == tag_id)
    )
    tag = tag.scalar()

    if not tag:
        raise HTTPException(status_code=404, detail='Tag not found')

    return [PostResponse.model_validate(p) for p in tag.posts]

@router.delete('/delete_post/{post_id}')
async def delete_post(post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await db.scalar(select(Post).where(Post.id == post_id))
    if post is None:
        raise HTTPException(status_code=404, detail='Post was not found')
    await db.execute(delete(Post).where(Post.id == post_id))
    await db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Post deleted successfuly!'}

@router.delete('/delete_posts')
async def delete_post(db: Annotated[AsyncSession, Depends(get_db)]):
    await db.execute(delete(Post))
    await db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Post deleted successfuly!'}