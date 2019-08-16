import time
from typing import Callable, List, Tuple, Dict, Any, Optional

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


SpriteAnimation = Callable[[RigidBody, SpriteAnimationData], SpriteImageTransformation]


def static_anim(static_index: int = 0) -> SpriteAnimation:
    return lambda body, sprite_data: SpriteImageTransformation(static_index)


def union_anim(sub_animations: List[SpriteAnimation]) -> SpriteAnimation:
    def impl(body, sprite_data):
        result = SpriteImageTransformation(sprite_data.current_image_index, custom_data=sprite_data.custom_data)
        for sub_animation in sub_animations:
            data = SpriteAnimationData(sprite_data.nb_images, custom_data=result.custom_data)
            data.current_image_index = result.sprite_index
            step = sub_animation(body, data)
            result = merge_transformations(step, result)
        return result
    return impl


def single_anim(duration: float) -> SpriteAnimation:
    end_time = time.time() + duration

    def impl(body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        now = time.time()
        time_to_live = max(end_time - now, 0)
        anim = (sprite_data.nb_images - 1) * (1 - time_to_live / duration)
        image_index = int(anim)
        return SpriteImageTransformation(image_index)
    return impl


def loop_anim(image_per_sec: float, intro_length: int = 0, outro_length: int = 0, total_duration: float = 0) -> SpriteAnimation:
    start_time = time.time()
    end_time = start_time + total_duration

    def impl(body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        now = time.time()
        if outro_length > 0:
            inv_index = int((end_time - now) / image_per_sec)
            if inv_index < outro_length:
                index = sprite_data.nb_images - inv_index - 1
                return SpriteImageTransformation(index)
        index = int((now - start_time) / image_per_sec)
        if index > intro_length:
            loop_length = sprite_data.nb_images - intro_length - outro_length
            index = intro_length + ((index - sprite_data.nb_images) % loop_length)
        return SpriteImageTransformation(index)
    return impl


def rotate_anim(rotation: float) -> SpriteAnimation:
    return lambda body, sprite_data: SpriteImageTransformation(sprite_data.current_image_index, rotation=rotation)


def flip_anim(vertical_flip: bool) -> SpriteAnimation:
    return lambda body, sprite_data: SpriteImageTransformation(sprite_data.current_image_index, vertical_flip=vertical_flip)


def sequence_anim(subanim_time: float, sub_animations: List[SpriteAnimation]) -> SpriteAnimation:
    def impl(body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        now = time.time()
        ratio = (now % subanim_time) / subanim_time
        i = int(ratio * len(sub_animations)) % len(sub_animations)
        return sub_animations[i](body, sprite_data)
    return impl


def switch_anim(cases: List[Tuple[Callable[[RigidBody], bool], SpriteAnimation]], default_case: SpriteAnimation) -> SpriteAnimation:
    def impl(body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        for case in cases:
            if case[0](body):
                return case[1](body, sprite_data)
        return default_case(body, sprite_data)
    return impl


def stateful_condition(condition: Callable[[RigidBody], Optional[bool]], sub_animation: SpriteAnimation) -> SpriteAnimation:
    animation_id = generate_unique_id()

    def impl(body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        condition_res = condition(body)
        if condition_res is None:
            if sprite_data.custom_data is not None and animation_id in sprite_data.custom_data:
                condition_res = sprite_data.custom_data[animation_id]
            else:
                return SpriteImageTransformation(sprite_data.current_image_index)
        custom_data = {animation_id: condition_res}
        result = SpriteImageTransformation(sprite_data.current_image_index, custom_data=custom_data)
        if condition_res:
            data = SpriteAnimationData(sprite_data.nb_images, custom_data=sprite_data.custom_data)
            data.current_image_index = result.sprite_index
            step = sub_animation(body, data)
            result = merge_transformations(step, result)
        return result

    return impl
