def make_payload(name, props):
    return {
        "id": 0,
        "jsonrpc": "2.0",
        "method": name,
        "params": {k: v for k, v in props.items() if v is not None},
    }
