# -*- coding: utf-8 -*-

"""
Enum Classes go here
    Copyright: SingerLinks Consulting LLC 2018-2019 - all rights reserved
    Confidential Material - Do Not Distribute - SingerLinks Consulting dba NodeEra Software
"""

from enum import Enum

class DataType(Enum):
    UNKNOWN = "Unknown"
    STRING = "String"
    INT = "Integer"
    FLOAT = "Float"
    BOOLEAN = "Boolean"
    POINTCARTESIAN = "Point-Cartesian"
    POINTWGS84 = "Point-WGS84"
    DATE = "Date"
    TIME = "Time"
    LOCALTIME = "LocalTime"
    DATETIME = "DateTime"
    LOCALDATETIME = "LocalDateTime"
    DURATION = "Duration"
    NODE = "Node"
    RELATIONSHIP = "Relationship"
    PATH = "Path"
