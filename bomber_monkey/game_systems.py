from bomber_monkey.features.board.board_display_system import BoardDisplaySystem
from bomber_monkey.features.bomb.bomb_explosion_system import BombExplosionSystem
from bomber_monkey.features.bomb.bomb_sound_system import BombSoundSystem
from bomber_monkey.features.display.display_system import DisplaySystem, SpriteDisplaySystem
from bomber_monkey.features.display.fps_display_system import FpsDisplaySystem
from bomber_monkey.features.display.score_display_system import PlayerScoreDisplaySystem
from bomber_monkey.features.keyboard.keyboard_system import KeyboardSystem
from bomber_monkey.features.lifetime.lifetime_system import LifetimeSystem
from bomber_monkey.features.physics.collision_system import PlayerCollisionSystem
from bomber_monkey.features.physics.physic_system import PhysicSystem
from bomber_monkey.features.player.banana_eating_system import BananaEatingSystem
from bomber_monkey.features.player.player_controller_system import PlayerControllerSystem
from bomber_monkey.features.player.player_killer_system import PlayerKillerSystem
from bomber_monkey.features.tile.tile_killer_system import TileKillerSystem
from bomber_monkey.states.in_game import GameState


def systems_provider(state: GameState):
    return [
        KeyboardSystem(),
        PlayerControllerSystem(),
        PlayerCollisionSystem(state.board),
        PhysicSystem(.8),

        BombExplosionSystem(state),
        TileKillerSystem(state.board, lambda body: state.factory.create_banana(body, state.conf.banana_drop_rate)),
        PlayerKillerSystem(state),

        BananaEatingSystem(state),
        LifetimeSystem(),

        BoardDisplaySystem(state.conf, state.conf.image_loader, state.screen, state.conf.tile_size),
        PlayerScoreDisplaySystem(state, state.screen),
        FpsDisplaySystem(state, state.screen),

        DisplaySystem(state.conf, state.conf.image_loader, state.screen),
        SpriteDisplaySystem(state.conf, state.conf.image_loader, state.screen),
        BombSoundSystem(state),
    ]
