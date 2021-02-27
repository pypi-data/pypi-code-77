#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from bapy import IP
from bapy import ip_addr
from bapy import ip_loc
from bapy import ip_loc_aio
from bapy import IPLoc
from bapy import IPv4
from bapy import localhost

from bapy.data.test_addr import *


def test_addr():
    assert isinstance(ip_addr(), IPv4)


def test_all():
    obj = IP(google_addr)
    assert obj.text == google_addr
    assert obj.loc.country_name == google_country_name
    assert obj.name == google_name
    assert obj.ssh is None
    assert obj.ping is None

    for obj in [IP(google_addr, ssh=True, ping=True), asyncio.run(IP.new(google_addr))]:
        assert obj.text == google_addr
        assert obj.loc.country_name == google_country_name
        assert obj.name == google_name
        assert obj.ssh is False
        assert obj.ping is True


def test_loc():
    assert ip_loc(google_addr)['country_name'] == google_country_name
    assert (asyncio.run(ip_loc_aio(google_addr)))['country_name'] == google_country_name
    assert IPLoc().country_name == 'Spain'
    assert (asyncio.run(IPLoc.new())).country_name == 'Spain'


def test_myip():
    obj = IP(ping=True)
    assert obj.loc.country_name == 'Spain'
    assert obj.ping is True


def test_ping():
    for obj in [IP(ping_addr, ping=True), asyncio.run(IP.new(ping_addr))]:
        assert obj.ping is False or obj.ping is None


def test_ssh():
    for obj in [IP(password_addr, ssh=True), asyncio.run(IP.new(password_addr))]:
        assert obj.ssh


def test_sort():
    sort = sorted([IP(), IP(password_addr), IP(google_addr), IP(localhost)])
    assert sort[0].text == google_addr
    assert sort[1].text == password_addr
    assert sort[2].text == IP().text
    assert sort[3].text == localhost
