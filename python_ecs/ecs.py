import time
from typing import List, Dict, Type, Set, Callable, Optional

from bomber_monkey.utils.timing import timing

ComponentId = int
EntityId = int


class Component(object):
    Type = Type['Component']

    def __init__(self) -> None:
        self.sim: Simulator = None
        self._cid = Simulator._generate_id()
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

    def entity(self) -> 'Entity':
        return self.sim.get(self.eid)

    @property
    def type_id(self) -> 'Component.Type':
        return self.__class__

    def delete(self):
        self.sim.delete_component(self)

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
        :param sim: the simulator that call the update function
        :param dt: delta time since last update
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
    def __init__(self, ecs: 'Simulator', eid: EntityId):
        self._sim = ecs
        self._eid = eid

    @property
    def eid(self) -> EntityId:
        return self._eid

    def get(self, ctype: Component.Type) -> Optional[Component]:
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

    def __hash__(self):
        return hash(self.eid)

    def __repr__(self):
        return str(self._eid)


class Simulator(object):
    _id_source = 0

    @staticmethod
    def _generate_id():
        Simulator._id_source += 1
        return Simulator._id_source

    def __init__(self, context):
        self.context = context
        self._systems = []  # type: List[System]
        self._components = {}  # type: Dict[Component.Type, Dict[EntityId,Component]]
        self._dead = set()  # type: Set[int]
        self._to_create = []
        self.on_create = []  # type: List[Callable[[Entity],None]]
        self.on_destroy = []  # type: List[Callable[[Entity],None]]
        self.last_update = None
        self.start_hooks = []  # type: List[Callable[[Simulator],None]]
        self._components_to_delete = {}  # type: Dict[Component.Type, List[Component]]

    def reset(self):
        self._systems.clear()
        self._components.clear()
        self._dead.clear()
        self._to_create.clear()
        self.on_create.clear()
        self.on_destroy.clear()
        self.start_hooks.clear()

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
        self._systems = systems
        return self

    def add_system(self, system: System):
        assert isinstance(system, System)
        self._systems.append(system)
        return self

    def update(self):
        dt = self._compute_delta_time()

        for start_hook in self.start_hooks:
            start_hook(self)

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
                    try:
                        with timing(f'system.{sys.__class__.__name__}.update'):
                            sys.update(self, dt, first_component, *other_components)
                    except Exception as e:
                        print('system error on update: {}'.format(str(sys)))
                        raise e

            self._delete_components(first)

        for k in self._dead:
            for _ in self.on_destroy:
                _(self.get(k))

        for k in self._dead:
            for _, components in self._components.items():
                if k in components:
                    del components[k]
        self._dead.clear()

    def _compute_delta_time(self):
        now = time.time()
        if not self.last_update:
            self.last_update = now
        dt = now - self.last_update
        self.last_update = now
        return dt

    def _add_component(self, component: Component):
        assert component.eid is not None
        component.sim = self
        eid = component.eid

        comp_type = component.type_id
        if comp_type not in self._components:
            self._components[comp_type] = {}

        self._components[comp_type][eid] = component

    def delete_component(self, component: Component):
        comp_type = component.type_id
        if comp_type in self._components:
            components = self._components[comp_type]
            eid = component.eid
            if eid in components:
                if comp_type not in self._components_to_delete:
                    self._components_to_delete[comp_type] = []
                self._components_to_delete[comp_type].append(component)

    def _delete_components(self, component_type: Component.Type):
        if component_type in self._components_to_delete:
            for component in self._components_to_delete[component_type]:
                del self._components[component_type][component.eid]
            self._components_to_delete[component_type].clear()

    def clear_components(self, component_type: Component.Type):
        if component_type in self._components:
            del self._components[component_type]
