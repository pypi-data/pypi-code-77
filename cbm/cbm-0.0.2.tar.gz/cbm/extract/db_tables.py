#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of CbM (https://github.com/ec-jrc/cbm).
# Author    : Guido Lemoine, Konstantinos Anastasakis
# Credits   : GTCAP Team
# Copyright : 2021 European Commission, Joint Research Centre
# License   : 3-Clause BSD


def tables_dict():
    tb = {
        "dc": {
            "name": "DIAS Catalogue",
            "table": "dias_catalogue",
            "desc": "",
            "sql": """
                CREATE table public.{}_dias_catalogue (
                id serial,
                obstime timestamp without time zone not null,
                reference character varying(120) not null,
                sensor character(2) not null,
                card character(2) not null,
                status character varying(12) DEFAULT 'ingested'::character varying not null,
                footprint public.geometry(Polygon,4326)
                );"""
        },
        "s2": {
            "name": "S2 signatures",
            "table": "s2_signatures",
            "desc": "",
            "sql": """
                CREATE table public.{}_s2_signatures (
                    pid int, 
                    obsid int, 
                    band char(2), 
                    count real, 
                    mean real,
                    std real,
                    min real,
                    max real,
                    p25 real,
                    p50 real,
                    p75 real
                );
                """
        },
        "bs": {
            "name": "S1 Backscattering",
            "table": "bs_signatures",
            "desc": "",
            "sql": """
                CREATE table public.{}_bs_signatures (
                    pid int, 
                    obsid int, 
                    band char(2), 
                    count real, 
                    mean real,
                    std real,
                    min real,
                    max real,
                    p25 real,
                    p50 real,
                    p75 real
                );
                """
        },
        "c6": {
            "name": "S1 6-day coherence",
            "table": "c6_signatures",
            "desc": "",
            "sql": """
                CREATE table public.{}_c6_signatures (
                    pid int, 
                    obsid int, 
                    band char(2), 
                    count real, 
                    mean real,
                    std real,
                    min real,
                    max real,
                    p25 real,
                    p50 real,
                    p75 real
                );
                """
        },
        "aois": {
            "name": "AOIs (Optional) - Regions or Municipalities",
            "table": "aois",
            "desc": "",
            "sql": """
                CREATE table public.{}_aois (
                    name text not null,
                    wkb_geometry public.geometry(Polygon,4326)
                );"""
        }
    }
    return tb