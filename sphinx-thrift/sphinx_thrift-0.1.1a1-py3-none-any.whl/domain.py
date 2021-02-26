import enum
import re
from dataclasses import dataclass
from itertools import groupby
from typing import (Any, Callable, Dict, Iterable, List, Optional, Tuple,
                    Union, cast)

from docutils import nodes
from docutils.parsers.rst.directives import flag, unchanged, unchanged_required
from sphinx import addnodes
from sphinx.addnodes import (desc_addname, desc_annotation, desc_content,
                             desc_name, desc_signature, desc_type,
                             pending_xref)
from sphinx.builders import Builder
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, Index, IndexEntry, ObjType
from sphinx.environment import BuildEnvironment
from sphinx.ext.autodoc import Documenter
from sphinx.locale import _
from sphinx.roles import XRefRole
from sphinx.util import docfields, logging
from sphinx.util.nodes import make_refnode

list_re = re.compile(r'^(list|set)<(.*)>$')
map_re = re.compile(r'^map<(.*),(.*)>$')


def make_desc_type(content: str) -> desc_type:
    return desc_type(content, content)


def parse_type(typename: str,
               inner_node: Callable[[str], nodes.Node]) -> List[nodes.Node]:
    typename = typename.replace(' ', '')
    m = list_re.match(typename)
    if m:
        return [inner_node(m.group(1) + '<')] + parse_type(
            m.group(2), inner_node) + [inner_node('>')]
    m = map_re.match(typename)
    if m:
        return [inner_node('map<')] + parse_type(m.group(1), inner_node) + [
            inner_node(', ')
        ] + parse_type(m.group(2), inner_node) + [inner_node('>')]
    return [
        pending_xref('',
                     inner_node(typename),
                     refdomain='thrift',
                     refexplicit=False,
                     reftarget=typename,
                     reftype='field')
    ]


class ThriftObjectKind(enum.Enum):
    Module = 'module'
    Constant = 'constant'
    TypeDef = 'typedef'
    Enum = 'enum'
    EnumField = 'enum_field'
    Struct = 'struct'
    StructField = 'struct_field'
    Exception = 'exception'
    ExceptionField = 'exception_field'
    Service = 'service'
    ServiceMethod = 'service_method'


@dataclass(frozen=True, unsafe_hash=True)
class Signature:
    kind: ThriftObjectKind
    name: str
    module: Optional[str]

    def __str__(self) -> str:
        if self.module is None:
            return f'{self.name}:{self.kind.value}'
        return f'{self.module}.{self.name}:{self.kind.value}'


@dataclass(frozen=True)
class ThriftObjectData:
    signature: Signature
    document: str


def _index_entry(
    object_description: str
) -> Callable[['ThriftDomain', str, str], Tuple[str, str, str, str,
                                                Optional[str]]]:
    def impl(domain: 'ThriftDomain', title: str,
             target: str) -> Tuple[str, str, str, str, Optional[str]]:
        return 'pair', f'{domain.object_types[object_description].lname} ; {title}', target, '', None

    return impl


_index_objects = {kind: _index_entry(kind.value) for kind in ThriftObjectKind}


class ThriftObject(ObjectDescription[Signature]):
    @property
    def kind(self) -> ThriftObjectKind:
        return ThriftObjectKind(self.objtype)

    def add_target_and_index(self, name: Signature, sig: str,
                             signode: desc_signature) -> None:
        if name not in self.state.document.ids:
            signode['names'].append(name)
            signode['ids'].append(name)
            signode['first'] = (not self.names)

            domain = cast(ThriftDomain, self.env.get_domain(self.domain))
            make_index = _index_objects.get(name.kind, None)
            if make_index is not None:
                self.indexnode['entries'].append(
                    make_index(domain, name.name, str(name)))
            self.state.document.note_explicit_target(signode)
            domain.add_thrift_object(ThriftObjectData(name, self.env.docname))


class ThriftModule(ThriftObject):
    def handle_signature(self, sig: str, signode: Any) -> Signature:
        signode += desc_annotation('module ', 'module ')
        signode += desc_name(sig, sig)
        return Signature(self.kind, sig, None)


class ThriftConstant(ThriftObject):
    required_arguments = 1
    option_spec = {'module': unchanged_required, 'type': unchanged_required}

    def handle_signature(self, sig: str, signode: desc_signature) -> Signature:
        signode += desc_annotation(self.objtype, self.objtype)
        module_name = self.options['module'] + '.'
        signode += desc_name(sig, sig)
        signode += desc_type(': ', ': ')
        signode.extend(parse_type(self.options['type'], make_desc_type))
        return Signature(self.kind, sig, self.options['module'])


class ThriftTypedef(ThriftObject):
    required_arguments = 1
    option_spec = {'module': unchanged_required, 'target': unchanged_required}

    def handle_signature(self, sig: str, signode: desc_signature) -> Signature:
        signode += desc_annotation(self.objtype, self.objtype)
        module_name = self.options['module'] + '.'
        signode += desc_name(sig, sig)
        signode += desc_type(' = ', ' = ')
        signode.extend(parse_type(self.options['target'], make_desc_type))
        return Signature(self.kind, sig, self.options['module'])


class ThriftEnum(ThriftObject):
    required_arguments = 1
    option_spec = {'module': unchanged_required}

    def handle_signature(self, sig: str, signode: desc_signature) -> Signature:
        signode += desc_annotation(self.objtype, self.objtype)
        module_name = self.options['module'] + '.'
        signode += desc_name(sig, sig)
        return Signature(self.kind, sig, self.options['module'])


class ThriftEnumField(ThriftObject):
    option_spec = {
        'module': unchanged_required,
        'enum': unchanged_required,
        'value': unchanged_required
    }

    def handle_signature(self, sig: str, signode: desc_signature) -> Signature:
        enum_name = self.options['enum'] + '.'
        signode += desc_addname(enum_name, enum_name)
        signode += desc_name(sig, sig)
        signode += desc_annotation(' = ' + self.options['value'],
                                   ' = ' + self.options['value'])
        return Signature(self.kind, enum_name + sig, self.options['module'])


class ThriftStruct(ThriftObject):
    required_arguments = 1
    option_spec = {'module': unchanged_required, 'exception': flag}

    def handle_signature(self, sig: str, signode: desc_signature) -> Signature:
        annotation = 'exception' if 'exception' in self.options else self.objtype
        signode += desc_annotation(annotation, annotation)
        module_name = self.options['module'] + '.'
        signode += desc_name(sig, sig)
        return Signature(self.kind, sig, self.options['module'])


class ThriftStructField(ThriftObject):
    required_arguments = 1
    option_spec = {
        'module': unchanged_required,
        'struct': unchanged_required,
        'type': unchanged_required
    }

    def handle_signature(self, sig: str, signode: desc_signature) -> Signature:
        annotation = 'field'
        signode += desc_annotation(annotation, annotation)
        struct_name = self.options['struct'] + '.'
        signode += desc_name(sig, sig)
        signode += desc_type(': ', ': ')
        signode.extend(parse_type(self.options['type'], make_desc_type))
        return Signature(self.kind, struct_name + sig, self.options['module'])


class ThriftService(ThriftObject):
    required_arguments = 1
    option_spec = {'module': unchanged_required}

    def handle_signature(self, sig: str, signode: desc_signature) -> Signature:
        annotation = 'service'
        signode += desc_annotation(annotation, annotation)
        module_name = self.options['module'] + '.'
        # signode += desc_addname(module_name, module_name)
        signode += desc_name(sig, sig)
        return Signature(self.kind, sig, self.options['module'])


def parameter_list(arg: str) -> List[Tuple[str, str]]:
    if arg is None:
        return []
    return [(p.split(';')[0], p.split(';')[1]) for p in arg.split()]


class ThriftServiceMethod(ThriftObject):
    required_arguments = 1
    option_spec = {
        'module': unchanged_required,
        'service': unchanged_required,
        'parameters': parameter_list,
        'exceptions': parameter_list,
        'return_type': unchanged_required,
        'oneway': flag
    }

    doc_field_types = [
        docfields.TypedField('parameter',
                             label='Parameters',
                             names=('param', ),
                             typenames=('type', ),
                             typerolename='field',
                             can_collapse=True),
        docfields.TypedField('exception',
                             label='Exceptions',
                             names=('throws', ),
                             typenames=('type', ),
                             typerolename='field',
                             can_collapse=True)
    ]

    def handle_signature(self, sig: str, signode: desc_signature) -> Signature:
        if 'oneway' in self.options:
            signode += desc_annotation('oneway', 'oneway')
        signode += desc_type(self.options['return_type'] + ' ',
                             self.options['return_type'] + ' ')
        service_name = self.options['service'] + '.'
        signode += desc_name(sig, sig)
        signode += desc_addname('(', '(')
        first = True
        for name, type_ in self.options['parameters']:
            if first:
                first = False
            else:
                signode += desc_addname(', ', ', ')
            signode.extend(parse_type(type_, make_desc_type))
            signode += make_desc_type(' ')
            signode += desc_addname(name, name)
        signode += desc_addname(')', ')')
        first = True
        if self.options['exceptions']:
            signode += desc_addname(' throws (', ' throws (')
        for name, type_ in self.options['exceptions']:
            if first:
                first = False
            else:
                signode += desc_addname(', ', ', ')
            signode.extend(parse_type(type_, make_desc_type))
            signode += make_desc_type(' ')
            signode += desc_addname(name, name)
        if self.options['exceptions']:
            signode += desc_addname(')', ')')
        return Signature(self.kind, service_name + sig, self.options['module'])


class ThriftXRefRole(XRefRole):
    def result_nodes(
            self, document: nodes.document, env: BuildEnvironment,
            node: nodes.Element, is_ref: bool
    ) -> Tuple[List[nodes.Node], List[nodes.system_message]]:
        if not is_ref:
            return [node], []

        make_index = _index_objects.get(ThriftObjectKind(node['reftype']),
                                        None)
        if make_index is not None:
            target_id = 'index-{}-{}'.format(
                env.new_serialno('index-{}'.format(node['reftarget'])),
                node['reftarget'])
            target = nodes.target('', '', ids=[target_id])
            document.note_explicit_target(target)

            index = addnodes.index()
            index['entries'] = [
                make_index(cast(ThriftDomain, env.get_domain('thrift')),
                           node['reftarget'], target_id)
            ]
            return [target, index, node], []
        return [node], []


class ThriftIndex(Index):
    name = 'modindex'
    localname = 'Thrift Index'
    shortname = 'Index'

    def generate(
        self,
        docnames: Iterable[str] = None
    ) -> Tuple[List[Tuple[str, List[IndexEntry]]], bool]:
        entries = []
        objects = cast(ThriftDomain, self.domain).thrift_objects
        for obj in objects:
            entries.append(
                IndexEntry(name=obj.signature.name,
                           subtype=0,
                           docname=obj.document,
                           anchor=str(obj.signature),
                           extra=self.domain.object_types[
                               obj.signature.kind.value].lname,
                           qualifier='',
                           descr=''))
        content: Dict[str, List[IndexEntry]] = {}
        for key, group in groupby(entries, key=lambda t: t[0][0].upper()):
            content.setdefault(key, []).extend(group)
        return sorted(content.items(), key=lambda t: t[0]), False


class ThriftDomain(Domain):
    name = 'thrift'
    object_types = {
        'module':
        ObjType(_('module'), 'module'),
        'namespace':
        ObjType(_('namespace'), 'namespace'),
        'constant':
        ObjType(_('constant'), 'constant'),
        'typedef':
        ObjType(_('type alias'), 'typedef'),
        'enum':
        ObjType(_('enumeration'), 'enum'),
        'enum_field':
        ObjType(_('enumerator'), 'enum_field'),
        'struct':
        ObjType(_('struct'), 'struct'),
        'struct_field':
        ObjType(_('struct field'), 'struct_field'),
        'exception':
        ObjType(_('exception'), 'struct', 'exception'),
        'exception_field':
        ObjType(_('exception field'), 'struct_field', 'exception_field'),
        'service':
        ObjType(_('service'), 'service'),
        'service_method':
        ObjType(_('service method'), 'service_method')
    }
    directives = {
        'module': ThriftModule,
        'constant': ThriftConstant,
        'typedef': ThriftTypedef,
        'enum': ThriftEnum,
        'enum_field': ThriftEnumField,
        'struct': ThriftStruct,
        'struct_field': ThriftStructField,
        'exception': ThriftStruct,
        'exception_field': ThriftStructField,
        'service': ThriftService,
        'service_method': ThriftServiceMethod
    }
    roles = {
        'module': ThriftXRefRole(),
        'constant': ThriftXRefRole(),
        'typedef': ThriftXRefRole(),
        'enum': ThriftXRefRole(),
        'enum_field': ThriftXRefRole(),
        'struct': ThriftXRefRole(),
        'struct_field': ThriftXRefRole(),
        'exception': ThriftXRefRole(),
        'exception_field': ThriftXRefRole(),
        'service': ThriftXRefRole(),
        'service_method': ThriftXRefRole()
    }
    indices = [ThriftIndex]
    initial_data: Dict[str, Any] = {'objects': []}

    def resolve_xref(self, env: BuildEnvironment, fromdocname: str,
                     builder: Builder, typ: str, target: str,
                     node: pending_xref,
                     contnode: nodes.Element) -> nodes.Element:
        def find_target() -> Optional[ThriftObjectData]:
            moduleless_results = []
            for obj in self.thrift_objects:
                if target.split('.') == [
                        obj.signature.module, obj.signature.name
                ]:
                    return obj
                if obj.signature.name == target:
                    moduleless_results.append(obj)
            if len(moduleless_results) == 1:
                return moduleless_results[0]
            elif len(moduleless_results) > 1:
                logger = logging.getLogger(__name__)
                logger.warning(
                    f'{target} is ambiguous. Possible resolutions:',
                    extra={
                        'resolutions':
                        list(str(obj.signature) for obj in moduleless_results)
                    })
            return None

        targetdata = find_target()
        if targetdata is not None:
            return make_refnode(builder, fromdocname, targetdata.document,
                                str(targetdata.signature), contnode)
        else:
            return None

    def merge_domaindata(self, docnames: List[str], otherdata: Dict) -> None:
        objects = cast(Iterable[ThriftObject], otherdata['objects'])
        for obj in objects:
            if obj.docname in docnames:
                self.add_thrift_object(obj)

    def add_thrift_object(self, obj: ThriftObjectData) -> None:
        cast(List[ThriftObjectData], self.data['objects']).append(obj)

    @property
    def thrift_objects(self) -> Iterable[ThriftObjectData]:
        return self.data['objects']
