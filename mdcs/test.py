# ./test.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2014-01-07 14:50:06.380509 by PyXB version 1.2.3
# Namespace AbsentNamespace0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:e8312da1-77d4-11e3-88b7-003ee1b763c3')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.3'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.CreateAbsentNamespace()
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, unicode):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Complex type Root with content type ELEMENT_ONLY
class Root (pyxb.binding.basis.complexTypeDefinition):
    """Complex type Root with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Root')
    _XSDLocation = pyxb.utils.utility.Location('/Users/ssy/Develop/Workspaces/mgi/static/resources/files/schemas/_choice.xsd', 6, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element choice uses Python identifier choice
    __choice = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'choice'), 'choice', '__AbsentNamespace0_Root_choice', False, pyxb.utils.utility.Location('/Users/ssy/Develop/Workspaces/mgi/static/resources/files/schemas/_choice.xsd', 8, 3), )

    
    choice = property(__choice.value, __choice.set, None, None)

    _ElementMap.update({
        __choice.name() : __choice
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'Root', Root)


# Complex type Choice with content type ELEMENT_ONLY
class Choice (pyxb.binding.basis.complexTypeDefinition):
    """Complex type Choice with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Choice')
    _XSDLocation = pyxb.utils.utility.Location('/Users/ssy/Develop/Workspaces/mgi/static/resources/files/schemas/_choice.xsd', 13, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element element1 uses Python identifier element1
    __element1 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'element1'), 'element1', '__AbsentNamespace0_Choice_element1', False, pyxb.utils.utility.Location('/Users/ssy/Develop/Workspaces/mgi/static/resources/files/schemas/_choice.xsd', 15, 4), )

    
    element1 = property(__element1.value, __element1.set, None, None)

    
    # Element element2 uses Python identifier element2
    __element2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, u'element2'), 'element2', '__AbsentNamespace0_Choice_element2', False, pyxb.utils.utility.Location('/Users/ssy/Develop/Workspaces/mgi/static/resources/files/schemas/_choice.xsd', 16, 9), )

    
    element2 = property(__element2.value, __element2.set, None, None)

    _ElementMap.update({
        __element1.name() : __element1,
        __element2.name() : __element2
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'Choice', Choice)


root = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'root'), Root, location=pyxb.utils.utility.Location('/Users/ssy/Develop/Workspaces/mgi/static/resources/files/schemas/_choice.xsd', 4, 3))
Namespace.addCategoryObject('elementBinding', root.name().localName(), root)



Root._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'choice'), Choice, scope=Root, location=pyxb.utils.utility.Location('/Users/ssy/Develop/Workspaces/mgi/static/resources/files/schemas/_choice.xsd', 8, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Root._UseForTag(pyxb.namespace.ExpandedName(None, u'choice')), pyxb.utils.utility.Location('/Users/ssy/Develop/Workspaces/mgi/static/resources/files/schemas/_choice.xsd', 8, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Root._Automaton = _BuildAutomaton()




Choice._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'element1'), pyxb.binding.datatypes.string, scope=Choice, location=pyxb.utils.utility.Location('/Users/ssy/Develop/Workspaces/mgi/static/resources/files/schemas/_choice.xsd', 15, 4)))

Choice._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'element2'), pyxb.binding.datatypes.string, scope=Choice, location=pyxb.utils.utility.Location('/Users/ssy/Develop/Workspaces/mgi/static/resources/files/schemas/_choice.xsd', 16, 9)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Choice._UseForTag(pyxb.namespace.ExpandedName(None, u'element1')), pyxb.utils.utility.Location('/Users/ssy/Develop/Workspaces/mgi/static/resources/files/schemas/_choice.xsd', 15, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Choice._UseForTag(pyxb.namespace.ExpandedName(None, u'element2')), pyxb.utils.utility.Location('/Users/ssy/Develop/Workspaces/mgi/static/resources/files/schemas/_choice.xsd', 16, 9))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Choice._Automaton = _BuildAutomaton_()

