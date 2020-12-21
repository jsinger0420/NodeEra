# -*- coding: utf-8 -*-

"""
Enum Classes go here
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
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
