from fastapi import FastAPI, HTTPException, status, Response
from fastapi.params import Body
from random import randrange
from pydantic import BaseModel


app = FastAPI()

my_posts = [
    {'id': 1, 'title': 'Python', 'content': 'Let\'s learn Python'},
    {'id': 2, 'title': 'SQL', 'content': 'Let\'s learn SQL'}
]


class Post(BaseModel):
    title: str
    content: str


def get_p(id: int):
    for p in my_posts:
        if p['id'] == id:
            return p


def get_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return None


@app.get('/')
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_all_posts():
    return {"data": my_posts}


@app.get("/posts/{id}")
def get_post(id: int):
    post = get_p(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"post with id: {id} was not found!"})
    return {"data": f'Here is post {id}'}


@app.post('/createpost', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(3, 100000)
    my_posts.append(post_dict)
    return {"data": f"Title: {post_dict['title']} Content: {post_dict['content']}"}


@app.delete('/deletepost/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = get_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} doesn't exist!")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/updatepost/{id}', status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int, post: Post):
    index = get_index_post(id)
    print(index)
    print(post)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found!")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
