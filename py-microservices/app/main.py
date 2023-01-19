# @klotho::execution_unit {
#   id = "microsrv-api"
# }

from app.model import get_user, post_user
from fastapi import FastAPI
from starlette.responses import PlainTextResponse

# @klotho::expose {
#   id = "microsrv-gw"
#   target = "public"
# }
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/{user_id}")
async def read_item(user_id: str):
    return await get_user(user_id)


@app.post("/users/{user_id}", response_class=PlainTextResponse)
async def write_user(user_id: str, tags: str=''):
    '''
    Upserts a user. The tags are comma-delimited, and come in two forms, which you can mix and match:
    
    - "flat" tags, which are just the tag name
    - "value" tags, which come in name=value format

    For example, /users/alice?tags=foo,bar,hello=world would create three tags:

    - "foo" (a flat tag)
    - "bar" (a flat tag)
    - "hello" => "world" (a value tag)
    ''' 
    flat_tags, value_tags = _parse_tags(tags)
    await post_user(user_id, *flat_tags, **value_tags)
    return f"Created {user_id}"

def _parse_tags(tags: str) -> (list[str], dict[str, str]):
    flat_tags = []
    value_tags = {}
    for tag in tags.split(','):
        if not tag:
            continue # ignore blank tags
        segments = tag.split('=', 1) # separate the tag by its first comma, if present
        if len(segments) == 1:
            flat_tags.append(tag)
        else:
            name, value = segments
            value_tags[name] = value
    return flat_tags, value_tags
