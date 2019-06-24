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
        self._ecs = ecs
        self._eid = eid

    @property
    def eid(self) -> EntityId:
        return self._eid

    def get(self, ctype: Component.Type) -> Component:
        components = self._ecs._components.get(ctype)
        if not components:
            return None
        return components.get(self.eid)

    def attach(self, component: Component):
        assert isinstance(component, Component)
        component.eid = self.eid
        self._ecs._add_component(component)
        return self


class ECS(object):
    _id_source = 0

    @staticmethod
    def _generate_id():
        ECS._id_source += 1
        return ECS._id_source

    def __init__(self):
        self._systems = []  # type: List[System]
        self._components = {}  # type: Dict[Component.Type, Dict[EntityId,Component]]

    def create(self, *components) -> Entity:
        entity = Entity(self, self._generate_id())
        for c in components:
            entity.attach(c)
        return entity

    def reset_systems(self, systems: List[System]):
        self._systems = systems
        return self

    def add_system(self, system: System):
        assert isinstance(system, System)
        self._systems.append(system)
        return self

    def update(self):
        for sys in self._systems:
            first, *others = sys.signature
            first_components = self._components[first]
            for eid, first_component in first_components.items():
                components_view = [self._components.get(_) for _ in others]
                components_view = filter(None.__ne__, components_view)
                other_components = [_.get(eid) for _ in components_view]
                other_components = list(filter(None.__ne__, other_components))

                if len(other_components) == len(others):
                    sys.update(first_component, *other_components)

    def _add_component(self, component: Component):
        assert component.eid is not None
        eid = component.eid

        comp_type = component.type_id
        if comp_type not in self._components:
            self._components[comp_type] = {}

        self._components[comp_type][eid] = component


# default simulator
sim = ECS()
