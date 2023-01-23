# @klotho::execution_unit {
#   id = "microsrv-users"
# }

from aiocache import Cache
from datetime import datetime


# @klotho::persist {
#   id = "users_data"
# }
__users = Cache(Cache.MEMORY)

async def get_user(id: str):
    user_info = await __users.get(id, default=False)
    if not user_info:
        return None
    # aiocache turns the "created"timestamp into a decimal.Decimal, so convert it back to a float
    created_dt = datetime.fromtimestamp(float(user_info["created"]))
    created_iso = created_dt.isoformat(timespec='seconds')
    return {
        "id": id,
        "created": created_iso,
        "tags": user_info["tags"]
    }


async def post_user(id: str, *flat_tags: str, **value_tags: str):
    await __users.set(id, {
        "created": datetime.utcnow().timestamp(),
        "tags": {
            "flat": flat_tags,
            "value": value_tags,
        },
    })
