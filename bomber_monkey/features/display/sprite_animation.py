import time
from abc import ABC, abstractmethod
from typing import List, Dict, Any

from bomber_monkey.features.physics.rigid_body import RigidBody

__unique_id = 0


def generate_unique_id() -> str:
    global __unique_id
    __unique_id = __unique_id + 1
    return str(__unique_id)


class SpriteAnimationData:
    def __init__(self, nb_images: int, custom_data: Dict[str, Any] = None):
        self.nb_images = nb_images
        self.current_image_index = 0
        self.custom_data = custom_data


class SpriteImageTransformation:

    def __init__(self, sprite_index: int = 0, rotation: float = 0, vertical_flip: bool = False,
                 custom_data: Dict[str, Any] = None):
        self.sprite_index = sprite_index
        self.rotation = rotation
        self.vertical_flip = vertical_flip
        self.custom_data = custom_data


class SpriteAnimation(ABC):
    def __init__(self, name: str = None, enabled: bool = True):
        self.name = name
        self.enabled = enabled

    def animate(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        if self.enabled:
            return self.do_animate(body, sprite_data)
        else:
            return SpriteImageTransformation()

    @abstractmethod
    def do_animate(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        ...


def merge_transformation_custom_data(transfo1: SpriteImageTransformation, transfo2: SpriteImageTransformation):
    if transfo1.custom_data is None:
        merged_data = transfo2.custom_data
    elif transfo2.custom_data is None:
        merged_data = transfo1.custom_data
    else:
        merged_data = {**transfo2.custom_data, **transfo1.custom_data}
    return merged_data


def merge_transformations(transfo1: SpriteImageTransformation, transfo2: SpriteImageTransformation):
    return SpriteImageTransformation(transfo1.sprite_index, transfo1.rotation + transfo2.rotation,
                                     transfo1.vertical_flip != transfo2.vertical_flip,
                                     custom_data=merge_transformation_custom_data(transfo1, transfo2))


class UnionAnim(SpriteAnimation):
    def __init__(self, sub_animations: List[SpriteAnimation], name: str = None, enabled: bool = True):
        super().__init__(name, enabled)
        self.sub_animations = sub_animations

    def do_animate(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        result = SpriteImageTransformation(sprite_data.current_image_index, custom_data=sprite_data.custom_data)
        for animation in self.sub_animations:
            if not animation.enabled:
                continue
            data = SpriteAnimationData(sprite_data.nb_images, custom_data=result.custom_data)
            data.current_image_index = result.sprite_index
            step = animation.animate(body, data)
            result = merge_transformations(step, result)
        return result

    def get_anim(self, name: str):
        return next(a for a in self.sub_animations if a.name == name)


class SingleAnim(SpriteAnimation):
    def __init__(self, duration: float, name: str = None, enabled: bool = True):
        super().__init__(name, enabled)
        self.duration = duration
        self.end_time = time.time() + duration

    def do_animate(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        now = time.time()
        time_to_live = max(self.end_time - now, 0)
        anim = (sprite_data.nb_images - 1) * (1 - time_to_live / self.duration)
        image_index = int(anim)
        return SpriteImageTransformation(image_index)


class StaticAnim(SpriteAnimation):
    def __init__(self, static_index: int = 0, name: str = None, enabled: bool = True):
        super().__init__(name, enabled)
        self.transformation = SpriteImageTransformation(static_index)

    def do_animate(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        return self.transformation


class LoopAnim(SpriteAnimation):
    def __init__(self, image_per_sec: float, intro_length: int = 0, outro_length: int = 0, total_duration: float = 0,
                 name: str = None, enabled: bool = True):
        super().__init__(name, enabled)
        self.image_per_sec = image_per_sec
        self.intro_length = intro_length
        self.outro_length = outro_length
        self.total_duration = total_duration
        self.start_time = time.time()
        self.end_time = self.start_time + total_duration

    def do_animate(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        now = time.time()
        if self.outro_length > 0:
            inv_index = int(max(self.end_time - now, 0) / self.image_per_sec)
            if inv_index < self.outro_length:
                index = sprite_data.nb_images - inv_index - 1
                return SpriteImageTransformation(index)
        index = int((now - self.start_time) / self.image_per_sec)
        if index > self.intro_length:
            loop_length = sprite_data.nb_images - self.intro_length - self.outro_length
            index = self.intro_length + ((index - sprite_data.nb_images) % loop_length)
        return SpriteImageTransformation(index)


class RotateAnim(SpriteAnimation):
    def __init__(self, rotation: float, name: str = None, enabled: bool = True):
        super().__init__(name, enabled)
        self.rotation = rotation

    def do_animate(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        return SpriteImageTransformation(sprite_data.current_image_index, rotation=self.rotation)


class FlipAnim(SpriteAnimation):
    def __init__(self, vertical_flip: bool, name: str = None, enabled: bool = True):
        super().__init__(name, enabled)
        self.vertical_flip = vertical_flip

    def do_animate(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        return SpriteImageTransformation(sprite_data.current_image_index, vertical_flip=self.vertical_flip)


class SequenceAnim(SpriteAnimation):
    def __init__(self, subanim_time: float, sub_animations: List[SpriteAnimation], name: str = None,
                 enabled: bool = True):
        super().__init__(name, enabled)
        self.subanim_time = subanim_time
        self.sub_animations = sub_animations

    def do_animate(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        now = time.time()
        ratio = (now % self.subanim_time) / self.subanim_time
        i = int(ratio * len(self.sub_animations)) % len(self.sub_animations)
        return self.sub_animations[i].animate(body, sprite_data)
