from typing import Any, Optional

from attr import Attribute, attrs, attrib
from attr.validators import instance_of, optional


def validate_greater_than_zero(instance: Any, attribute: Attribute, value: Optional[int]) -> None:
    if value is not None and value <= 0:
        raise ValueError(f"{attribute.name} cannot be less than one, found: {value}")


@attrs(frozen=True, kw_only=True)
class ToyReadStyle(object):
    height: Optional[int] = attrib(
        default=None, validator=[validate_greater_than_zero, optional(instance_of(int))]
    )
    width: Optional[int] = attrib(
        default=None, validator=[validate_greater_than_zero, optional(instance_of(int))]
    )
    padding: int = attrib(default=20, validator=[validate_greater_than_zero, instance_of(int)])
