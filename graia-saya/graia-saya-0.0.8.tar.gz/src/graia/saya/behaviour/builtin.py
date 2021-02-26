from typing import Any, Generic, TypeVar
from .entity import Router

T = TypeVar("T")

class MountPoint(Router, Generic[T]):
    def __init__(self, route_point: str, target: T) -> None:
        self.route_point = route_point
        self.target = target
    
    def route(self, route: str) -> T:
        if route == self.route_point:
            return self.target