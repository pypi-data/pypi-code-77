# -*- coding:utf-8 -*-
"""
Sections organize movement between pages in an experiment.

.. moduleauthor:: Johannes Brachem <jbrachem@posteo.de>, Paul Wiemann <paulwiemann@gmail.com>
"""

from . import element as elm
from ._core import ExpMember
from ._helper import inherit_kwargs
from .page import _PageCore, UnlinkedDataPage, _DefaultFinalPage
from .exceptions import AlfredError, ValidationError, AbortMove
from . import alfredlog
from random import shuffle

@inherit_kwargs
class Section(ExpMember):
    """
    The basic section, allows forward and backward movements.

    Args:
        shuffle (bool): If True, the order of all members in this 
            section will be randomized every time the section is entered.
            Shuffling is not recursive, it only affects direct members
            of a section. That means, if there are subsections, 
            their position in the parent section will be randomized, 
            but the members within the subsection will not be affected. 
            Defaults to False. Can be defined as a class attribute.
        {kwargs}
    
    Examples:
        Using a basic section and filling it with a page in instance 
        style::

            import alfred3 as al
            exp = al.Experiment()

            exp += al.Section(name="main")
            
            exp.main += al.Page(title="Demo", name="DemoPage")
        
        Using a basic section and filling it with a page in class style::

            import alfred3 as al
            exp = al.Experiment()

            @exp.member
            class Main(al.Section): pass

            @exp.member(of_section="Main")
            class DemoPage(al.Page):
                title = "Demo"

    """

    #: Controls, whether participants can move forward from pages in 
    #: this section.
    allow_forward: bool = True

    #: Controls, whether participants can move backward from pages in 
    #: this section.
    allow_backward: bool = True
    
    #: Controls, whether participants can jump *from* pages in this 
    #: section
    allow_jumpfrom: bool = True
    
    #: Controls, whether participants can jump *to* pages in this 
    #: section.
    allow_jumpto: bool = True

    #: If True, the members of this section will be randomized every
    #: time the section is entered.
    shuffle: bool = False

    def __init__(self, title: str = None, name: str = None, shuffle: bool = None, **kwargs):
        super().__init__(title=title, name=name, **kwargs)

        self.members = {}
        self._should_be_shown = True
        
        #: bool: Boolean flag, indicating whether the experiment session
        #: is currently operating within this section
        self.active: bool = False

        if shuffle is not None:
            self.shuffle = shuffle
    
    def __contains__(self, member):
        try:
            return member.name in self.all_members or member.name in self.all_elements
        except AttributeError:
            return member in self.all_members or member in self.all_elements

    def __repr__(self):
        return f"Section(class='{type(self).__name__}', name='{self.name}')"

    def __iadd__(self, other):
        self.append(other)
        return self
    
    def __getitem__(self, name):
        return self.all_members[name]
    
    def __getattr__(self, name):
        try:
            return self.all_members[name]
        except KeyError:
            return AttributeError(f"{self} has no attribute '{name}'.")

    def shuffle_members(self):
        """Non-recursive shuffling of this section's members."""

        members = list(self.members.items())
        shuffle(members)
        self.members = dict(members)
    
    @property
    def all_updated_members(self) -> dict:
        """ 
        Returns a dict of all members that already have exp access.
        """
        return {name: m for name, m in self.all_members.items() if m.exp is not None}
    
    @property
    def all_updated_pages(self) -> dict:
        pages = {}
        for name, member in self.all_updated_members.items():
            if isinstance(member, _PageCore):
                pages[name] = member
        
        return pages
    
    @property
    def all_updated_elements(self) -> dict:
        elements = {}
        for page in self.all_updated_pages.values():
            elements.update(page.updated_elements)
        return elements

    @property
    def all_members(self) -> dict:
        """
        Returns a flat dict of all members in this section and its subsections.

        The order is preserved, i.e. members are listed in this dict in 
        the same order in which they appear in the experiment.
        """
        members = {}

        for name, member in self.members.items():
            members[name] = member
            if isinstance(member, Section):
                members.update(member.all_members)
        
        return members

    @property
    def last_member(self):
        return list(self.members.values())[-1]
    
    @property
    def first_member(self):
        return list(self.members.values())[0]

    @property
    def all_subsections(self) -> dict:
        """
        Returns a flat dict of all sections in this section and its subsections.

        The order is preserved, i.e. sections are listed in this dict in 
        the same order in which they appear in the experiment.
        """
        subsections = {}

        for name, member in self.members.items():
            if isinstance(member, Section):
                subsections[name] = member
                subsections.update(member.all_subsections)
        
        return subsections

    @property
    def subsections(self) -> dict:
        """
        Returns a flat dict of all subsections in this section.

        Subsections in subsections are not included. Use 
        :attr:`.all_subsections` for that purpose.
        """
        return {name: sec for name, sec in self.members.items() if isinstance(sec, Section)}

    @property
    def all_pages(self) -> dict:
        """
        Returns a flat dict of all pages in this section and its subsections.

        The order is preserved, i.e. pages are listed in this dict in 
        the same order in which they appear in the experiment.
        """

        pages = {}
        for name, member in self.members.items():
            if isinstance(member, _PageCore):
                pages[name] = member
            elif isinstance(member, Section):
                pages.update(member.all_pages)
        
        return pages
    
    @property
    def all_closed_pages(self) -> dict:
        return {name: page for name, page in self.all_pages.items() if page.is_closed}
    
    @property
    def all_shown_pages(self) -> dict:
        return {name: page for name, page in self.all_pages.items() if page.has_been_shown}
    
    @property
    def pages(self) -> dict:
        """
        Returns a flat dict of all pages in this section.

        Pages in subsections are not included. Use :attr:`.all_pages`
        for that purpose.
        """
        return {name: page for name, page in self.members.items() if isinstance(page, _PageCore)}
    
    @property
    def all_elements(self) -> dict:
        """
        Returns a flat dict of all elements in this section.
        
        Recursive: Includes elements from pages in this section and all 
        its subsections.
        """

        elements = {}
        for page in self.all_pages.values():
            elements.update(page.elements)
        return elements
    
    @property
    def all_input_elements(self) -> dict:
        """
        Returns a flat dict of all input elements in this section.
        
        Recursive: Includes elements from pages in this section and all 
        its subsections.
        """

        elements = {}
        for page in self.all_pages.values():
            elements.update(page.input_elements)
        return elements
    
    @property
    def all_shown_input_elements(self) -> dict:
        """
        Returns a flat dict of all shown input elements in this section.
        
        Recursive: Includes elements from pages in this section and all 
        its subsections.
        """

        elements = {}
        for page in self.all_pages.values():
            if page.has_been_shown:
                elements.update(page.input_elements)
        return elements
    
    @property
    def data(self):
        data = {}
        for page in self.all_pages.values():
            data.update(page.data)
        return data
    
    @property
    def unlinked_data(self):
        data = {}
        for page in self.all_pages.values():
            data.update(page.unlinked_data)
        
        return data
    
    @property
    def unlinked_element_data(self):
        data = {}
        for page in self.all_pages.values():
            data.update(page.unlinked_element_data)
        
        return data

    def added_to_experiment(self, exp):
        super().added_to_experiment(exp)
        self.log.add_queue_logger(self, __name__)
        self.on_exp_access()
        self.update_members_recursively()
    
    def update_members(self):
        
        for member in self.members.values():
            if not member.experiment:
                member.added_to_experiment(self.exp)
            if not member.section:
                member.added_to_section(self)
    
    def update_members_recursively(self):

        self.update_members()

        for member in self.members.values():
            member.update_members_recursively()
    
    def generate_unset_tags_in_subtree(self):
        for i, member in enumerate(self.members.values(), start=1):
            
            if member.tag is None:
                member.tag = str(i)
            
            if isinstance(member, Section):
                member.generate_unset_tags_in_subtree()

    def append(self, *items):
        for item in items:

            if item.name in dir(self):
                raise ValueError(f"Name of {item} is also an attribute of {self}.")
            
            if item.name in self.members:
                raise AlfredError(f"Name '{item.name}' is already present in the experiment.")

            item.added_to_section(self)

            self.members[item.name] = item
            
            if self.experiment is not None:
                item.added_to_experiment(self.experiment)
                item.update_members_recursively()
            
            if not item.tag:
                item.tag = str(len(self.members) + 1)


    def on_exp_access(self):
        """
        Executed *once*, when the :class:`.ExperimentSession` becomes 
        available to the section.

        See Also:
            See :ref:`hooks-how-to` for a how to on using hooks and an overview
            of available hooks.

        """
        pass

    def on_enter(self):
        """
        Executed *every time* this section is entered.

        See Also:
            See :ref:`hooks-how-to` for a how to on using hooks and an overview
            of available hooks.
        """
        pass

    def on_leave(self):
        """
        Executed *every time* this section is left.

        See Also:
            See :ref:`hooks-how-to` for a how to on using hooks and an overview
            of available hooks.
        """
        pass

    def on_resume(self):
        """ 
        Executed *every time* the experiment resumes from a direct subsection to this section.

        Resuming takes place, when a child section is left and the
        next page is a direct child of the parent section. Then this 
        the parent section becomes the primary current section again: it
        resumes its status.

        See Also:
            See :ref:`hooks-how-to` for a how to on using hooks and an overview
            of available hooks.
        """
        pass

    def on_hand_over(self):
        """
        Executed *every time* a direct subsection of this section is entered.

        See Also:
            See :ref:`hooks-how-to` for a how to on using hooks and an overview
            of available hooks.
        
        """
        pass

    def enter(self):
        self.active = True
        
        self.log.debug(f"Entering {self}.")
        self.on_enter()
        self.update_members()

        if self.shuffle:
            self.shuffle_members()

        if isinstance(self.first_member, Section) and not self.first_member.active:
            self.hand_over()
            self.first_member.enter()
        
    def leave(self):
        self.log.debug(f"Leaving {self}.")
        self.on_leave()

        self.validate_on_leave()
        for page in self.pages.values():
            page.close()
        
        if self is self.parent.last_member:
            self.parent.leave()
    
    def resume(self):
        self.log.debug(f"Resuming to {self}.")
        self.on_resume()
    
    def hand_over(self):
        self.log.debug(f"{self} handing over to child section.")
        self.on_hand_over()
    
    def forward(self):
        pass
    
    def backward(self):
        pass
    
    def jumpfrom(self):
        pass
    
    def jumpto(self):
        pass

    def move(self, direction):
        """
        Conducts a section's part of moving in an alfred experiment.

        Raises:
            ValidationError: If validation of the current page fails.
        """
        self.validate_on_move()
        
        if direction == "forward":
            self.forward()
        elif direction == "backward":
            self.backward()
        elif direction == "jumpfrom":
            self.jumpfrom()
        elif direction == "jumpto":
            self.jumpto()
        
        if self.exp.aborted:
            raise AbortMove
        

    def validate_on_leave(self):
        """
        Validates pages and their input elements within the section.

        Can be overloaded to change the validating behavior of a derived
        section.

        Notes:
            Validation is conducted only for pages that are direct 
            children of this section. Pages in subsections are not 
            validated.

        Raises:
            ValidationError: If validation fails.
        """
        for page in self.pages.values():
            
            if not page.validate_page():
                raise ValidationError()

            if not page.validate_elements():
                msg = self.exp.config.get("hints", "no_input_section_validation")
                msg = msg.format(n=len(self.pages))
                self.exp.post_message(msg, level="danger")
                raise ValidationError()

    def validate_on_move(self):
        """
        Validates the current page and its elements.

        Can be overloaded to change the validating behavior of a derived
        section.

        Raises:
            ValidationError: If validation fails.
        """
        
        if not self.exp.current_page.validate_page():
            raise ValidationError()
        
        if not self.exp.current_page.validate_elements():
            raise ValidationError()
        

@inherit_kwargs
class RevisitSection(Section):
    """
    A section that disables all input elements upon moving forward (and
    jumping) form it, but still allows participants to revisit previous
    pages.

    Args:
        {kwargs}

    Examples:
        Using a RevisitSection and filling it with a page in instance 
        style::

            import alfred3 as al
            exp = al.Experiment()

            exp += al.RevisitSection(name="main")
            
            exp.main += al.Page(title="Demo", name="DemoPage")
        
        Using a basic section and filling it with a page in class style::

            import alfred3 as al
            exp = al.Experiment()

            @exp.member
            class Main(al.RevisitSection): pass

            @exp.member(of_section="Main")
            class DemoPage(al.Page):
                title = "Demo"
    """
    allow_forward: bool = True
    allow_backward: bool = True
    allow_jumpfrom: bool = True
    allow_jumpto: bool = True

    def forward(self):
        super().forward()
        self.exp.movement_manager.current_page.close()
    
    def jumpfrom(self):
        super().jumpfrom()
        self.exp.movement_manager.current_page.close()

@inherit_kwargs
class OnlyForwardSection(RevisitSection):
    """
    A section that allows only a single step forward; no jumping and no
    backwards steps.

    Args:
        {kwargs}
    
    Examples:
        Using an OnlyForwardSection and filling it with a page in instance 
        style::

            import alfred3 as al
            exp = al.Experiment()

            exp += al.OnlyForwardSection(name="main")
            
            exp.main += al.Page(title="Demo", name="DemoPage")
        
        Using a basic section and filling it with a page in class style::

            import alfred3 as al
            exp = al.Experiment()

            @exp.member
            class Main(al.OnlyForwardSection): pass

            @exp.member(of_section="Main")
            class DemoPage(al.Page):
                title = "Demo"
    """
    allow_forward: bool = True
    allow_backward: bool = False
    allow_jumpfrom: bool = False
    allow_jumpto: bool = False


@inherit_kwargs
class _FinishedSection(Section):
    """
    A section that finishes the experiment on entering it.
    
    Args:
        {kwargs}
    """

    allow_forward: bool = False
    allow_backward: bool = False
    allow_jumpfrom: bool = False
    allow_jumpto: bool = True

    def enter(self):
        super().enter()
        self.experiment.finish()

class _AbortSection(Section):
    allow_forward: bool = False
    allow_backward: bool = False
    allow_jumpfrom: bool = False
    allow_jumpto: bool = True


@inherit_kwargs
class _RootSection(Section):
    """
    A section that serves as parent for all other sections in the 
    experiment. 

    Args:
        {kwargs}
    
    Defines the '_content' section and the '__finished_section' as its 
    only direct children.
    """

    name = "_root"

    def __init__(self, experiment):
        super().__init__()
        self._experiment = experiment
        self.log.add_queue_logger(self, __name__)
        self.content = Section(name="_content")
        self.finished_section = _FinishedSection(name="__finished_section")
        self.finished_section += _DefaultFinalPage(name="_final_page")

        self._all_pages_list = None
        self._all_page_names = None
    
    def append_root_sections(self):
        self += self.content
        self += self.finished_section
    
    @property
    def all_page_names(self):
        """Improvised caching mechanism for the list of all page names."""

        if not self._all_page_names:
            self._all_page_names = list(self.all_pages.keys())

        elif not len(self._all_page_names) == len(self.all_pages):
            self._all_page_names = list(self.all_pages.keys())
        
        return self._all_page_names
    
    @property
    def all_pages_list(self):
        """Improvised caching mechanism for the list of all pages."""

        if not self._all_pages_list:
            self._all_pages_list = list(self.all_pages.values())

        elif not len(self._all_pages_list) == len(self.all_pages):
            self._all_pages_list = list(self.all_pages.values())
        
        return self._all_pages_list
    
    @property
    def final_page(self):
        return self.finished_section._final_page

    @final_page.setter
    def final_page(self, page):
        page += elm.misc.HideNavigation()
        self.finished_section.members = {}
        self.finished_section._final_page = page
    
