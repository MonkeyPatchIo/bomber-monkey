import time
from typing import Callable, List, Tuple

from bomber_monkey.features.physics.rigid_body import RigidBody


class SpriteAnimationData:
    def __init__(self, nb_images: int):
        self.nb_images = nb_images
        self.current_image_index = 0


class SpriteImageTransformation:

    def __init__(self, sprite_index: int = 0, rotation: float = 0, vertical_flip: bool = False):
        self.sprite_index = sprite_index
        self.rotation = rotation
        self.vertical_flip = vertical_flip


class SpriteAnimation:

    def next(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        raise NotImplementedError()


class StaticSpriteAnimation(SpriteAnimation):

    def __init__(self, static_index: int = 0):
        self.static_index = static_index

    def next(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        return SpriteImageTransformation(self.static_index)


class UnionSpriteAnimation(SpriteAnimation):

    def __init__(self, sub_animations: List[SpriteAnimation]):
        self.sub_animations = sub_animations

    def next(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        result = SpriteImageTransformation(sprite_data.current_image_index)
        for sub_animation in self.sub_animations:
            data = SpriteAnimationData(sprite_data.nb_images)
            data.current_image_index = result.sprite_index
            step = sub_animation.next(body, data)
            result = SpriteImageTransformation(step.sprite_index, step.rotation + result.rotation,
                                               step.vertical_flip != result.vertical_flip)
        return result


class SingleSpriteAnimation(SpriteAnimation):

    def __init__(self, duration: float):
        self.duration = duration
        self.end_time = time.time() + duration

    def next(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        now = time.time()
        time_to_live = max(self.end_time - now, 0)
        anim = (sprite_data.nb_images - 1) * (1 - time_to_live / self.duration)
        image_index = int(anim)
        return SpriteImageTransformation(image_index)


class LoopSpriteAnimation(SpriteAnimation):

    def __init__(self, anim_time: float):
        self.anim_time = anim_time
        self.start_time = time.time()

    def next(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        now = time.time()
        index = int((now - self.start_time) / self.anim_time)
        image_index = index % sprite_data.nb_images
        return SpriteImageTransformation(image_index)


class LoopWithIntroSpriteAnimation(SpriteAnimation):

    def __init__(self, anim_time: float, intro_length: int):
        self.anim_time = anim_time
        self.start_time = time.time()
        self.intro_length = intro_length

    def next(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        now = time.time()
        index = int((now - self.start_time) / self.anim_time)
        if index > self.intro_length:
            loop_length = sprite_data.nb_images - self.intro_length
            index = self.intro_length + ((index - sprite_data.nb_images) % loop_length)
        return SpriteImageTransformation(index)


class RotateSpriteAnimation(SpriteAnimation):

    def __init__(self, rotation: float):
        self.rotation = rotation

    def next(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        return SpriteImageTransformation(sprite_data.current_image_index, rotation=self.rotation)


class FlipSpriteAnimation(SpriteAnimation):

    def __init__(self, vertical_flip: Callable[[RigidBody], bool]):
        self.vertical_flip = vertical_flip

    def next(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        return SpriteImageTransformation(sprite_data.current_image_index, vertical_flip=self.vertical_flip(body))


class SequencedSpriteAnimation(SpriteAnimation):

    def __init__(self, anim_time: float, sub_animations: List[SpriteAnimation]):
        self.anim_time = anim_time
        self.sub_animations = sub_animations

    def next(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        now = time.time()
        ratio = (now % self.anim_time) / self.anim_time
        i = int(ratio * len(self.sub_animations)) % len(self.sub_animations)
        return self.sub_animations[i].next(body, sprite_data)


class SwitchSpriteAnimation(SpriteAnimation):

    def __init__(self, cases: List[Tuple[Callable[[RigidBody], bool], SpriteAnimation]], default_case: SpriteAnimation):
        self.cases = cases
        self.default_case = default_case

    def next(self, body: RigidBody, sprite_data: SpriteAnimationData) -> SpriteImageTransformation:
        for case in self.cases:
            if case[0](body):
                return case[1].next(body, sprite_data)
        return self.default_case.next(body, sprite_data)

