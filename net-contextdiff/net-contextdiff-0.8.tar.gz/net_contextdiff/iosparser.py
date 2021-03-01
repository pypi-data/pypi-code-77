# iosparser.py
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Cisco IOS configuration module.

This module parses Cisco IOS configuration files into a dictionary.
"""



# --- imports ---



from netaddr import IPNetwork

import re
import sys

from .configparser import (
    IndentedContextualCommand, IndentedContextualConfig, pathsetdefault)



# --- constants ---



# interface names and their canonical representations - the canonical
# versions don't have to be how Cisco IOS always displays them, in any
# particular context, but just so they can consistently matched against

_INTERFACE_CANONICALS = {
    "ethernet": "Eth",
    "fastethernet": "Fa",
    "gigabitethernet": "Gi",
    "tengigabitethernet": "Te",
    "fortygigabitethernet": "Fo",
    "port-channel": "Po",
    "vl": "Vlan"
}



# _SERVICE_PORTS = dict
#
# Dictionary mapping service names (as displayed/usable in an access-
# list rule) into a port number.

_SERVICE_PORTS = {
    "bootps": 67,
    "bootpc": 68,
    "discard": 9,
    "domain": 53,
    "ftp": 21,
    "ftp-data": 20,
    "gopher": 70,
    "ident": 113,
    "isakmp": 500,
    "lpd": 515,
    "mail": 25,
    "non500-isakmp": 4500,
    "ntp": 123,
    "smtp": 25,
    "snmp": 161,
    "tftp": 69,
    "www": 80
}



# --- functions ---



def _expand_set(s):
    """This function exapands a string giving a set of numbers,
    separated by commas, which can include ranges from low to high,
    using hyphens.  The return value will be the set of numbers
    expressed.

    For example, given a string of "1,3-5", a set containing 1, 3, 4
    and 5 will be returned.
    """

    t = set()

    for i in s.split(","):
        i_range = i.split("-")

        if len(i_range) == 1:
            t.add(int(i))
        else:
            t.update(range(int(i_range[0]), int(i_range[1]) + 1))

    return t



def _ipnet4_to_ios(ipnet4):
    """This method converts an IPv4 IPNetwork object into its canonical
    representation in Cisco IOS in a standard access-list.

    Conversions are '0.0.0.0/0' to 'any' and single host networks (i.e.
    simple addresses) into a plain address with no mask.
    """

    if ipnet4 == IPNetwork("0.0.0.0/0"):
        return "any"

    if ipnet4.prefixlen == 32:
        return str(ipnet4.ip)

    return str(ipnet4.ip) + " " + str(ipnet4.hostmask)



def _service_to_port(service):
    """Converts a Cisco service named 'service' (as displayed/usable in
    an access-list rule) into a port number and return it as an
    integer.

    If the service name is not defined, it is assumed to already be
    numeric and is converted to an integer and returned.  If this
    conversion fails, an exception will be raised (whch probably
    indicates a service that is missing from the list).
    """

    return _SERVICE_PORTS.get(service) or int(service)



# IPV4 STANDARD ACCESS CONTROL LIST RULES



# regular expression for matching an IPv4 standard ACL rule, compiled
# once for efficiency

_ACL4_STD_RULE_RE = re.compile(
    r"^"
    r"(?P<action>permit|deny)"
    r" +"

    # we match "0.0.0.0 255.255.255.255" as "any" because the
    # netaddr module assumes the mask is a netmask (= /32) rather
    # than a hostmask, in this case
    r"((?P<any>any|0\.0\.0\.0 255\.255\.255\.255)|"
        r"(?:host )?(?P<host>[0-9.]+)|"
        r"(?P<net>[0-9.]+) (?P<mask>[0-9.]+))"

    r"$")


def _acl4_std_rule_parse(rule):
    """Parse an IPv4 standard ACL rule, returning a 2-element tuple
    consisting of the action ('permit' or 'deny') and an IPNetwork
    object, specifying the address/network to match.
    """


    match = _ACL4_STD_RULE_RE.match(rule)

    if not match:
        raise ValueError(
            "failed to parse IPv4 standard ACL rule: " + rule)


    # match some special cases and, if not those, match as a
    # network/hostmask

    if match.group("any"):
        ipnet4 = IPNetwork("0.0.0.0/0")

    elif match.group("host"):
        ipnet4 = IPNetwork(match.group("host"))

    else:
        ipnet4 = IPNetwork(match.group("net") + "/" + match.group("mask"))


    return match.group("action"), ipnet4



# IPV4 EXTENDED ACCESS CONTROL LIST RULES



# regular expression for matching an IPv4 extended ACL rule, compiled
# once for efficiency

_ACL4_EXT_RULE_RE = re.compile(
    r"^"
    r"(?P<action>permit|deny)"
    r" +"
    r"(?P<protocol>ip|icmp|tcp|udp|igmp|pim|gre|esp)"
    r" "
    r"(?P<src_addr>any|host ([0-9.]+)|([0-9.]+) ([0-9.]+))"
    r"( ("
        # 'eq' and 'neq' can support a list of services - we need to match
        # them non-greedy
        r"((?P<src_port_listop>eq|neq) (?P<src_port_list>\S+( \S+)*?))|"

        r"((?P<src_port_1op>lt|gt) (?P<src_port_num>\S+))|"
        r"range (?P<src_port_low>\S+) (?P<src_port_high>\S+)"
    r"))?"
    r" "
    r"(?P<dst_addr>any|host ([0-9.]+)|([0-9.]+) ([0-9.]+))"
    r"( ("
        r"((?P<dst_port_listop>eq|neq) (?P<dst_port_list>\S+( \S+)*?))|"
        r"((?P<dst_port_1op>lt|gt) (?P<dst_port_num>\S+))|"
        r"range (?P<dst_port_low>\S+) (?P<dst_port_high>\S+)|"
        r"(?P<icmp_type>echo(-reply)?)"
    r"))?"
    r"(?P<established> established)?"
    r"(?P<qos> (dscp \S+))?"
    r"(?P<log> (log|log-input))?"
    r"$"
)


def _acl4_ext_rule_parse(rule):
    """Parse an IPv4 extended ACL rule, returning a 'normalised'
    form of the rule as a string.  The normalised form should allow
    two ACL rules which mean the same thing to be compared using a
    simple string comparison.

    This process mainly involves extracting the port entries and
    [potentially] translating them into port numbers, if they're named
    services (which can be used in rules, plus IOS will translate a
    numbered service to a name, if one matches).

    Note that no attempt is made to check the rule for validity.
    """


    match = _ACL4_EXT_RULE_RE.match(rule)

    if not match:
        raise ValueError(
            "failed to parse IPv4 extended ACL rule: " + rule)


    action, protocol, src_addr, dst_addr = match.group(
        "action", "protocol", "src_addr", "dst_addr")


    # match.group() will return an error if a named group does not exist
    # in the regexp; match.groupdict(), however, will return a default
    # value (None, if not specified) for named groups that do not exist
    #
    # as such, we need to check if the retrieved groups are blank or
    # not, for optional/alternative parts of a rule

    groups = match.groupdict()


    src_port = ""

    if groups["src_port_listop"]:
        # if 'eq' or 'neq' was found for the source port, it will be one
        # or more services, separated by spaces - we need to split the
        # list up and turn each one into a port number, then join the
        # list back together again

        src_port = (
            " %s %s" % (
                groups["src_port_listop"],
                " ".join([str(_service_to_port(s))
                              for s
                              in groups["src_port_list"].split(" ")])))

    elif groups["src_port_1op"]:
        src_port = " %s %d" % (
                       groups["src_port_1op"],
                       _service_to_port(groups["src_port_num"]))

    elif groups["src_port_low"]:
        src_port = " range %d %d" % (
                        _service_to_port(groups["src_port_low"]),
                        _service_to_port(groups["src_port_high"]))


    dst_port = ""

    if groups["dst_port_listop"]:
        dst_port = (
            " %s %s" % (
                groups["dst_port_listop"],
                " ".join([str(_service_to_port(s))
                              for s
                              in groups["dst_port_list"].split(" ")])))

    elif groups["dst_port_1op"]:
        dst_port = " %s %d" % (
                        groups["dst_port_1op"],
                        _service_to_port(groups["dst_port_num"]))

    elif groups["dst_port_low"]:
        dst_port = " range %d %d" % (
                        _service_to_port(groups["dst_port_low"]),
                        _service_to_port(groups["dst_port_high"]))

    # the destination port could also be an ICMP message type
    elif groups["icmp_type"]:
        dst_port = " " + groups["icmp_type"]


    established = groups["established"] or ""

    qos = groups["qos"] or ""

    log = groups["log"] or ""


    return (action + " " + protocol
            + " " + src_addr + src_port
            + " " + dst_addr + dst_port + established + qos + log)



# IPV6 EXTENDED ACCESS CONTROL LIST RULES



# regular expression for matching an IPv6 access-list rule, compiled
# once for efficiency
#
# TODO: we know this doesn't match some of the more complicated rules
# (such as the CP policing ones matching ICMPv6 types) but we're
# excluding those in the output, anyway, so we just ignore them - as
# such, we don't match the end of string ('$')

_ACL6_RULE_RE = re.compile(
    r"^"
    r"(?P<action>permit|deny)"
    r"( "
        r"(?P<protocol>ipv6|icmp|tcp|udp|\d+)"
    r")?"
    r" "
    r"(?P<src_addr>any|host [0-9A-Fa-f:]+|[0-9A-Fa-f:]+/\d+)"
    r"( ("
        r"((?P<src_port_1op>eq|lt|gt|neq) (?P<src_port_num>\S+))|"
        r"range (?P<src_port_low>\S+) (?P<src_port_high>\S+)"
    r"))?"
    r" "
    r"(?P<dst_addr>any|host [0-9A-Fa-f:]+|[0-9A-Fa-f:]+/\d+)"
    r"( ("
        r"((?P<dst_port_1op>eq|lt|gt|neq) (?P<dst_port_num>\S+))|"
        r"range (?P<dst_port_low>\S+) (?P<dst_port_high>\S+)|"
        r"(?P<icmp_type>echo(-reply)?)"
    r"))?"
    r"(?P<established> established)?"
    r"(?P<log> (log|log-input))?"
)


def _acl6_rule_parse(rule):
    """Parse an IPv6 ACL rule, returning a 'normalised' form of the rule
    as a string.  The normalised form should allow two ACL rules which
    mean the same thing to be compared using a simple string comparison.

    This process mainly involves extracting the port entries and
    [potentially] translating them into port numbers, if they're named
    services (which can be used in rules, plus IOS will translate a
    numbered service to a name, if one matches).

    Note that no attempt is made to check the rule for validity.
    """


    match = _ACL6_RULE_RE.match(rule)

    if not match:
        raise ValueError("failed to parse IPv6 ACL rule: " + rule)


    action, protocol, src_addr, dst_addr = match.group(
        "action", "protocol", "src_addr", "dst_addr")


    # if the protocol was not specified, we default to 'ipv6'

    if protocol is None:
        protocol = "ipv6"


    # lower case the source and destination addresses since IPv6
    # addresses can either be in upper or lower case (usually upper, in
    # IOS); we choose lower here, though, to avoid upper-casing the
    # keywords 'host' and 'any'

    src_addr = src_addr.lower()
    dst_addr = dst_addr.lower()


    # match.group() will return an error if a named group does not exist
    # in the regexp; match.groupdict(), however, will return a default
    # value (None, if not specified) for named groups that do not exist
    #
    # as such, we need to check if the retrieved groups are blank or
    # not, for optional/alternative parts of a rule

    groups = match.groupdict()


    src_port = ""

    if groups["src_port_num"]:
        src_port = " %s %d" % (
                       groups["src_port_1op"],
                       _service_to_port(groups["src_port_num"]))

    elif groups["src_port_low"]:
        src_port = " range %d %d" % (
                       _service_to_port(groups["src_port_low"]),
                       _service_to_port(groups["src_port_high"]))


    dst_port = ""

    if groups["dst_port_num"]:
        dst_port = " %s %d" % (
                       groups["dst_port_1op"],
                       _service_to_port(groups["dst_port_num"]))

    elif groups["dst_port_low"]:
        dst_port = " range %d %d" % (
                       _service_to_port(groups["dst_port_low"]),
                       _service_to_port(groups["dst_port_high"]))


    elif groups["icmp_type"]:
        dst_port = " " + groups["icmp_type"]


    established = groups["established"] or ""

    log = groups["log"] or ""


    return (action + " " + protocol
            + " " + src_addr + src_port
            + " " + dst_addr + dst_port + established)



# --- configuration command classes ---



# _cmds = []
#
# This is a list of classes, one for each IOS configuration mode
# command.  The command classes are defined at the global level and
# added to this list.
#
# The CiscoIOSConfig class adds these to the object upon instantiation,
# by the _add_commands() method.
#
# This was done to make it clearer how the commands are implemented.

_cmds = []



# _Cmd is created to be a shorthand for the IndentedContextualCommand
# class as we'll be using it a lot

_Cmd = IndentedContextualCommand



# SYSTEM



class _Cmd_Comment(_Cmd):
    cmd = r"!.*"

_cmds.append(_Cmd_Comment)


class _Cmd_Hostname(_Cmd):
    cmd = r"hostname (?P<hostname>\S+)"

    def action(self, groups, cfg, params):
        cfg["hostname"] = groups["hostname"]

_cmds.append(_Cmd_Hostname)


class _Cmd_VLAN(_Cmd):
    cmd = r"vlan (?P<tag>\d+)"
    enter_context = "vlan"

    def action(self, groups, cfg, params):
        tag = int(groups["tag"])

        cfg_vlan = pathsetdefault(cfg, "vlans", tag)
        cfg_vlan.setdefault("options", set()).add("exists")

        return cfg_vlan

_cmds.append(_Cmd_VLAN)


class _CmdContext_VLAN(_Cmd):
    context = "vlan"

class _Cmd_VLAN_Name(_CmdContext_VLAN):
    cmd = r"name (?P<name>\S+)"

    def action(self, groups, cfg, params):
        cfg["name"] = groups["name"]

_cmds.append(_Cmd_VLAN_Name)



# SPANNING TREE



class _Cmd_NoSTP(_Cmd):
    cmd = r"no spanning-tree vlan (?P<tags>[-0-9,]+)"

    def action(self, groups, cfg, params):
        cfg.setdefault("no-stp", set()).update(_expand_set(groups["tags"]))

_cmds.append(_Cmd_NoSTP)


class _Cmd_STPPriority(_Cmd):
    cmd = r"spanning-tree vlan (?P<tags>[-0-9,]+) priority (?P<priority>\d+)"

    def action(self, groups, cfg, params):
        priority = groups["priority"]

        cfg_stp_pri = cfg.setdefault("stp-priority", {})
        for tag in _expand_set(groups["tags"]):
            cfg_stp_pri[tag] = priority

_cmds.append(_Cmd_STPPriority)



# INTERFACES



class _Cmd_Int(_Cmd):
    cmd = r"interface (?P<name>\S+)"
    enter_context = "interface"

    def action(self, groups, cfg, params):
        name = groups["name"]

        # we need to canonicalise the type of an interface as they can
        # be specified in various shorthand forms, and in mixed case
        #
        # the canonical form is '<type><number>'; the type is first
        # character capitalised
        #
        # TODO: we really should handle this more flexibly, with a
        # central funcation matching regexps of the interface name
        match = re.match(r"^([-a-z]+)([0-9/.]*)$", name.lower())
        if match:
            _type, num = match.groups()
            _type = _INTERFACE_CANONICALS.get(_type, _type).capitalize()
            name = _type + num

        return pathsetdefault(cfg, "interfaces", name)

_cmds.append(_Cmd_Int)


class _CmdContext_Int(_Cmd):
    context = "interface"


class _Cmd_Int_CDPEna(_CmdContext_Int):
    cmd = r"(?P<no>no )?cdp enable"

    def action(self, groups, cfg, params):
        cfg_opts = cfg.setdefault("options", set())

        # we allow this option to enable or disable the setting (if it's
        # already been set differently)
        if not groups["no"]:
            cfg_opts.add("cdp")
        else:
            cfg_opts.discard("cdp")

_cmds.append(_Cmd_Int_CDPEna)


class _Cmd_Int_ChnGrp(_CmdContext_Int):
    cmd = r"channel-group (?P<id>\d+)(?P<mode> .+)?"

    def action(self, groups, cfg, params):
        cfg["chgrp"] = groups["id"], groups["mode"]

_cmds.append(_Cmd_Int_ChnGrp)


class _Cmd_Int_Desc(_CmdContext_Int):
    cmd = r"description (?P<description>.+)"

    def action(self, groups, cfg, params):
        cfg["description"] = groups["description"]

_cmds.append(_Cmd_Int_Desc)


class _Cmd_Int_Encap(_CmdContext_Int):
    cmd = r"encapsulation (?P<encap>dot1q \d+( native)?)"

    def action(self, groups, cfg, params):
        # lower case the encapsulation definition as IOS stores 'dot1q'
        # as 'dot1Q'
        cfg["encap"] = groups["encap"].lower()

_cmds.append(_Cmd_Int_Encap)


class _Cmd_Int_HlprAddr(_CmdContext_Int):
    cmd = r"ip helper-address (?P<helper_addr>(global )?\S+)"

    def action(self, groups, cfg, params):
        cfg.setdefault("ip-helper-addr", set()).add(groups["helper_addr"])

_cmds.append(_Cmd_Int_HlprAddr)


class _Cmd_Int_IPAccGrp(_CmdContext_Int):
    cmd = r"ip access-group (?P<access_group>\S+) (?P<direction>in|out)"

    def action(self, groups, cfg, params):
        cfg.setdefault("ip-access-group", {})[groups["direction"]] = (
            groups["access_group"])

_cmds.append(_Cmd_Int_IPAccGrp)


class _Cmd_Int_IPAddr(_CmdContext_Int):
    cmd = r"ip address (?P<addr>\S+) (?P<netmask>\S+)"

    def action(self, groups, cfg, params):
        cfg["ip-address"] = groups["addr"], groups["netmask"]

_cmds.append(_Cmd_Int_IPAddr)


class _Cmd_Int_IPAddrSec(_CmdContext_Int):
    cmd = r"ip address (?P<addr>\S+) (?P<netmask>\S+) secondary"

    def action(self, groups, cfg, params):
        # secondary address - record it in a list
        cfg.setdefault("ip-address-secondary", set()).add(
            (groups["addr"], groups["netmask"]))

_cmds.append(_Cmd_Int_IPAddrSec)


class _Cmd_Int_IP6Addr(_CmdContext_Int):
    cmd = r"ipv6 address (?P<addr>\S+)"

    def action(self, groups, cfg, params):
        # IPv6 addresses involve letters so we lower case for
        # consistency
        cfg.setdefault("ipv6-address", set()).add(groups["addr"].lower())

_cmds.append(_Cmd_Int_IP6Addr)


class _Cmd_Int_VRF(_CmdContext_Int):
    cmd = (r"vrf forwarding (?P<vrf>\S+)")

    def action(self, groups, cfg, params):
        cfg["vrf-forwarding"] = groups["vrf"]

_cmds.append(_Cmd_Int_VRF)


class _Cmd_Int_ServPol(_CmdContext_Int):
    cmd = r"service-policy (?P<policy>.+)"

    def action(self, groups, cfg, params):
        cfg.setdefault("service-policy", set()).add(groups["policy"])

_cmds.append(_Cmd_Int_ServPol)


class _Cmd_Int_Shutdown(_CmdContext_Int):
    cmd = r"(?P<no>no )?shutdown"

    def action(self, groups, cfg, params):
        cfg_opts = cfg.setdefault("options", set())

        # set the 'shutdown' option, or remove it, if already set and
        # disabled
        if not groups["no"]:
            cfg_opts.add("shutdown")
        else:
            cfg_opts.discard("shutdown")

_cmds.append(_Cmd_Int_Shutdown)


class _Cmd_Int_SwPortTrkNtv(_CmdContext_Int):
    cmd = r"switchport trunk native vlan (?P<vlan>\d+)"

    def action(self, groups, cfg, params):
        cfg["swport-trk-ntv"] = groups["vlan"]

_cmds.append(_Cmd_Int_SwPortTrkNtv)


class _Cmd_Int_SwPortTrkAlw(_CmdContext_Int):
    cmd = r"switchport trunk allowed vlan (add )?(?P<vlans>[0-9,-]+)"

    def action(self, groups, cfg, params):
        cfg.setdefault("swport-trk-alw", set()).update(
            _expand_set(groups["vlans"]))

_cmds.append(_Cmd_Int_SwPortTrkAlw)


class _Cmd_Int_XConn(_CmdContext_Int):
    cmd = r"xconnect (?P<remote>[0-9.]+ \d+ .+)"

    def action(self, groups, cfg, params):
        cfg["xconnect"] = groups["remote"]

_cmds.append(_Cmd_Int_XConn)



# IPV4 AND IPV6 STATIC ROUTES


class _Cmd_IPRoute(_Cmd):
    cmd = r"ip route (?P<route>.+)"

    def action(self, groups, cfg, params):
        cfg.setdefault("route4", set()).add(groups["route"])

_cmds.append(_Cmd_IPRoute)


class _Cmd_IP6Route(_Cmd):
    cmd = r"ipv6 route (?P<route>.+)"

    def action(self, groups, cfg, params):
        # IPv6 addresses involve letters so we lower case for
        # consistency
        cfg.setdefault("route6", set()).add(groups["route"].lower())

_cmds.append(_Cmd_IP6Route)



# ACCESS LISTS (IPV4 STANDARD)



class _Cmd_ACLStdRule(_Cmd):
    cmd = r"access-list (?P<num>\d{1,2}|1[3-9]\d{2}) (?P<rule>.+)"

    def action(self, groups, cfg, params):
        cfg._acl4_std_add_rule(groups["num"], groups["rule"])

_cmds.append(_Cmd_ACLStdRule)


class _Cmd_IPACLStd(_Cmd):
    cmd = r"ip access-list standard (?P<name>.+)"
    enter_context = "acl4-std"

    def action(self, groups, cfg, params):
        name = groups["name"]

        pathsetdefault(cfg, "acl4-std", name, last=[])

        params["name"] = name

_cmds.append(_Cmd_IPACLStd)


class _Cmd_IPACLStd_Rule(_Cmd):
    context = "acl4-std"
    cmd = r"(?P<rule>(permit|deny) +.+)"

    def action(self, groups, cfg, params):
        cfg._acl4_std_add_rule(params["name"], groups["rule"])

_cmds.append(_Cmd_IPACLStd_Rule)


class _Cmd_ACLExtRule(_Cmd):
    cmd = r"access-list (?P<num>1\d{2}|2[0-6]\d{2}) (?P<rule>.+)"

    def action(self, groups, cfg, params):
        name = groups["num"]

        pathsetdefault(cfg, "acl4-ext", name, last=[]).append(
            _acl4_ext_rule_parse(groups["rule"]))

_cmds.append(_Cmd_ACLExtRule)


class _Cmd_IPACLExt(_Cmd):
    cmd = r"ip access-list extended (?P<name>.+)"
    enter_context = "acl4-ext"

    def action(self, groups, cfg, params):
        name = groups["name"]

        return pathsetdefault(cfg, "acl4-ext", name, last=[])

_cmds.append(_Cmd_IPACLExt)


class _Cmd_IPACLExt_Rule(_Cmd):
    context = "acl4-ext"
    cmd = r"(?P<rule>(permit|deny) +.+)"

    def action(self, groups, cfg, params):
        cfg.append(_acl4_ext_rule_parse(groups["rule"]))

_cmds.append(_Cmd_IPACLExt_Rule)



# ACCESS LISTS (IPV6)



class _Cmd_IP6ACL(_Cmd):
    cmd = r"ipv6 access-list (?P<name>.+)"
    enter_context = "acl6"

    def action(self, groups, cfg, params):
        name = groups["name"]

        return pathsetdefault(cfg, "acl6", name, last=[])

_cmds.append(_Cmd_IP6ACL)


class _Cmd_IP6ACL_Rule(_Cmd):
    context = "acl6"
    cmd = r"(?P<rule>(permit|deny) +.+)"

    def action(self, groups, cfg, params):
        cfg.append(_acl6_rule_parse(groups["rule"]))

_cmds.append(_Cmd_IP6ACL_Rule)



# PREFIX LISTS (IPV4 AND IPV6)



class _Cmd_IPPfx(_Cmd):
    cmd = r"ip prefix-list (?P<list>\S+) (seq \d+ )?(?P<rule>.+)"

    def action(self, groups, cfg, params):
        list_ = groups["list"]

        pathsetdefault(cfg, "pfx4", list_, last=[]).append(groups["rule"])

_cmds.append(_Cmd_IPPfx)


class _Cmd_IP6Pfx(_Cmd):
    cmd = r"ipv6 prefix-list (?P<list>\S+) (seq \d+ )?(?P<rule>.+)"

    def action(self, groups, cfg, params):
        list_ = groups["list"]

        pathsetdefault(cfg, "pfx6", list_, last=[]).append(
            groups["rule"].lower())

_cmds.append(_Cmd_IP6Pfx)



# --- classes ----



# class CiscoIOSConfigParser()
#
# This is the concrete class to parse Cisco IOS configuration files.


class CiscoIOSConfig(IndentedContextualConfig):
    "This class parses Cisco IOS configuration files."



    def _add_commands(self):
        """This method is called by the constructor to add commands for
        the IOS platform.

        The commands are stored in a global (to the module) level list
        of classes.
        """

        for cmd_class in _cmds:
            self._add_command(cmd_class)


    def _post_parse_file(self):
        """Extend the inherited method to flush any pending IPv4
        standard ACL rules into the configuration.
        """

        super()._post_parse_file()

        # go through the pending IPv4 standard ACLs and store them (we
        # convert this to a list as _acl4_std_flush() will change the
        # dictionary during iteration and we only need the names)
        for id in list(self.get("acl4-std-pending", {})):
            self._acl4_std_flush(id)


    def _acl4_std_add_rule(self, id, rule):
        """This method adds a rule to an IPv4 standard access control
        list.  The name (or number) of ACL is supplied, along with the
        rule in string form.  The rule will be parsed into the action
        and address portions.

        IPv4 standard ACLs are complicated IOS due to its tendency to
        reorganise the rules.  It always preserves the semantics of the
        the rules (never putting an overlapping 'permit' and 'deny' in
        the wrong order, but can move rules which don't interact around.
        Presumably this is done to optimise processing.

        The solution adopted here is to build the ACL up in 'blocks'.
        Each block is a set of rules where the address portions don't
        overlap - these are built up and then, finally, sorted into
        numeric address order, before storing.

        When a rule is read which has an address portion that overlaps
        one of the rules in the current ("pending") block so far, the
        existing rules are sorted and stored, then a new block begun
        with the new rule.  This is done by _acl4_std_flush().

        This results in lists which are not necessarily in the same
        order as they were constructed, nor how IOS is storing them, but
        two lists should at least be the same so they can be compared.

        After parsing the entire configuration, any 'pending' blocks
        still be built must be flushed using _acl4_std_flush().  The
        _post_parse_file() method does this.
        """

        action, ipnet4 = _acl4_std_rule_parse(rule)

        # create parts of the configuration, if they don't exist
        self.setdefault("acl4-std-pending", {})
        self["acl4-std-pending"].setdefault(id, set())

        # check if there is an overlap with the address part of a rule
        # in the current block
        overlap = [None for _, check_ipnet4
                        in self["acl4-std-pending"][id]
                        if ((ipnet4.first <= check_ipnet4.last)
                            and (ipnet4.last >= check_ipnet4.first))]

        # if there was an overlap, store the pending block and create a
        # new, empty one
        if overlap:
            self._acl4_std_flush(id)
            self["acl4-std-pending"][id] = set()

        # add this rule to the pending block (either the existing one,
        # or a new one)
        self["acl4-std-pending"][id].add((action, ipnet4))


    def _acl4_std_flush(self, id):
        """This method stores the current, pending, IPv4 standard access
        control lists into the configuration and deletes them from the
        pending list (so if any further rules are added, a new "pending"
        block will need to be created first).

        The rules are first sorted, into address order, then converted
        into IOS textual format.
        """

        # sort the rules in the current block based on the address
        # portion (the second tuple) and then convert them to text form
        rules = [(action + " " + _ipnet4_to_ios(ipnet4))
                    for action, ipnet4
                    in sorted(self["acl4-std-pending"][id],
                            key=(lambda rule: rule[1]))]

        # create parts of the configuration, if they don't exist
        self.setdefault("acl4-std", {})
        self["acl4-std"].setdefault(id, [])
        self["acl4-std"][id].extend(rules)

        # delete the current block (it will need to be recreated with
        # an empty set, if it is required)
        self["acl4-std-pending"].pop(id)
