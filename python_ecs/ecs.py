import time
from typing import List, Dict, Type

ComponentId = int
EntityId = int


class Component(object):
    Type = Type['Component']

    def __init__(self) -> None:
        self._cid = ECS._generate_id()
        self._eid = None  # type: EntityId

    @property
    def cid(self) -> ComponentId:
        return self._cid

    @property
    def eid(self) -> EntityId:
        return self._eid

    @eid.setter
    def eid(self, eid: EntityId):
        self._eid = eid

    @property
    def type_id(self) -> 'Component.Type':
        return self.__class__

    def __hash__(self):
        return hash(self.cid)

    def __eq__(self, other):
        return isinstance(other, Component) and self._cid == other.cid


class System(object):
    Signature = List[Type['Component']]

    Type = Type['System']

    def __init__(self, component_signature: 'System.Signature'):
        """
        :param component_signature: list of component type ids as return by Component.type_id
        """
        self._signature = component_signature

    def update(self, *args, **kwargs) -> None:
        """
        :param args: components in same order as the System.signature
        :param kwargs: named parameter list : 'Component.type_id = component' (ex: MyComponent = component_instance))
        :return:
        """
        raise NotImplementedError()

    @property
    def signature(self) -> 'System.Signature':
        return self._signature

    @property
    def type_id(self) -> 'System.Type':
        return self.__class__


class Entity(object):
    def __init__(self, ecs: 'ECS', eid: EntityId):
        self._sim = ecs
        self._eid = eid

    @property
    def eid(self) -> EntityId:
        return self._eid

    def get(self, ctype: Component.Type) -> Component:
        components = self._sim._components.get(ctype)
        if not components:
            return None
        return components.get(self.eid)

    def attach(self, component: Component):
        assert isinstance(component, Component)
        component.eid = self.eid
        self._sim._add_component(component)
        return self

    def destroy(self):
        self._sim._dead.add(self.eid)

    def __eq__(self, other):
        return isinstance(other, Entity) and self._eid == other.eid


class TimeDelta:

    def __init__(self):
        self._value = 0.0

    def update(self):
        self._value += 1

    @property
    def value(self) -> float:
        return self._value


class RealTimeDelta(TimeDelta):

    def __init__(self):
        super().__init__()
        self._last_update_time = None

    def update(self):
        t = time.time()
        self._value = 0.1 if self._last_update_time is None else t - self._last_update_time
        self._last_update_time = t


class ECS(object):
    _id_source = 0

    @staticmethod
    def _generate_id():
        ECS._id_source += 1
        return ECS._id_source

    def __init__(self):
        self.reset()

    def create(self, *components) -> Entity:
        entity = Entity(self, self._generate_id())
        self._to_create.append((entity, components))
        return entity

    def _create_now(self, entity, components) -> None:
        for c in components:
            entity.attach(c)
        for _ in self.on_create:
            _(entity)
        return entity

    def get(self, eid: int) -> Entity:
        return Entity(self, eid)

    def reset_systems(self, systems: List[System]):
        for system in systems:
            self.add_system(system)
        return self

    def reset(self):
        self._systems = []  # type: List[System]
        self._components = {}  # type: Dict[Component.Type, Dict[EntityId,Component]]
        self._dead = set()  #  type: Set[int]
        self._to_create = []
        self.on_create = []  # type: List[Callable[[Entity],None]]
        self.on_destroy = []  # type: List[Callable[[Entity],None]]
        self._time_delta = RealTimeDelta()

    def add_system(self, system: System):
        assert isinstance(system, System)
        set_time_delta = getattr(system, "set_time_delta", None)
        if callable(set_time_delta):
            set_time_delta(self._time_delta)
        self._systems.append(system)
        return self

    def update(self):
        self._time_delta.update()

        for k in self._to_create:
            self._create_now(*k)
        self._to_create.clear()

        for sys in self._systems:
            first, *others = sys.signature
            if not first in self._components:
                continue
            first_components = self._components[first]
            for eid, first_component in first_components.items():
                components_view = [self._components.get(_) for _ in others]
                components_view = filter(None.__ne__, components_view)
                other_components = [_.get(eid) for _ in components_view]
                other_components = list(filter(None.__ne__, other_components))

                if len(other_components) == len(others):
                    sys.update(first_component, *other_components)

        for k in self._dead:
            for _ in self.on_destroy:
                _(self.get(k))

        for k in self._dead:
            for _, components in self._components.items():
                if k in components:
                    del components[k]
        self._dead.clear()

    def _add_component(self, component: Component):
        assert component.eid is not None
        eid = component.eid

        comp_type = component.type_id
        if comp_type not in self._components:
            self._components[comp_type] = {}

        self._components[comp_type][eid] = component


# default simulator
sim = ECS()
