from tatu.abs.storage import DuplicateEntryException
from tatu.okast import OkaSt, default_url

from oka.client import oka


def get(uuid, url=default_url, token=None):
    token = token or oka.token
    okast = OkaSt(token=token, url=url, close_when_idle=True)
    oka.token = okast.token
    data = okast.fetch(uuid, lazy=False)  # TODO make laziness work
    if not data:
        print(f"[Error] Data with OID {uuid} was not found.")
        return None

    return data


def send(data, url=default_url, token=None, name=None, description="No description"):
    # TODO: how to solve post stored but data failed: check if orphan post exist, and delete it from the begining?
    token = token or oka.token

    # Create inactive Post.
    name = name or "→".join(
        x[:3] for x in data.history ^ "name" if x[:3] not in ["B", "Rev", "In", "Aut", "E"]
    )
    info = {
        "nattrs": data.X.shape[1],
        "ninsts": data.X.shape[0],
        "ntargs": data.Y.shape[1] if len(data.Y.shape) > 1 else 1,
        "nclasses": len(set(data.y)),
        "past": list(data.past)
    }
    dic = {'data_uuid': data.id, "info": info, "name": name, "description": description}

    try:
        okast = OkaSt(token=token, url=url, close_when_idle=True)
        okast.request("/api/posts", "put", json=dic)
        oka.token = okast.token
        okast.store(data, lazy=False)
        # Activate Post.
        okast.request("/api/posts/activate", "put", json={'data_uuid': data.id})
    except DuplicateEntryException as e:
        print(f"[Error] You have already uploaded the dataset with OID {e}.")

    return True
