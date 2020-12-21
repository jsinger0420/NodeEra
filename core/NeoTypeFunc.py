# -*- coding: utf-8 -*-

"""
Class implementing datatype conversion functions.
 
Copyright 2018-2020 SingerLinks Consulting LLC 

This file is part of NodeEra.

NodeEra is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

NodeEra is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with NodeEra. If not, see <https://www.gnu.org/licenses/>.
 
"""

#from neo4j import 
#from neotime import Date, DateTime, Time, Duration
import neo4j.time
from neo4j.time import Date, DateTime,  Time, Duration
from neo4j.spatial import CartesianPoint, WGS84Point
from neo4j.graph import Node, Relationship, Path
from core.Enums import DataType
from dateutil.parser import parse

class NeoTypeFunc():
    '''
    This class provides functions needed to convert Neo4j values and datatypes to/from QT usable strings
    '''

    def getNeo4jDataType(self, value=None):
        '''
        value is a data item returned by a cypher query.
        This function returns the Enum representing the neo4j type for the value
            POINTCARTESIAN = "Point-Cartesian"
            POINTWGS84 = "Point-WGS84"
        '''
        try:
            if isinstance(value, str):
                return DataType.STRING.value
            if isinstance(value, bool):
                return DataType.BOOLEAN.value
            if isinstance(value, int):
                return DataType.INT.value
            if isinstance(value, float):
                return DataType.FLOAT.value
            if isinstance(value, Node):
                return DataType.NODE.value
            if isinstance(value, Relationship):
                return DataType.RELATIONSHIP.value
            if isinstance(value, Path):
                return DataType.PATH.value     
            if isinstance(value, Duration):
                return DataType.DURATION.value       
            if isinstance(value, Time):
                # time and localtime use the same class Time so we have to figure out which one it is.
                if value.tzinfo is None:
                    return DataType.LOCALTIME.value
                else:
                    return DataType.TIME.value
            if isinstance(value, Date):
                return DataType.DATE.value
            if isinstance(value, DateTime):
                # datetime and localdatetime use the same class DateTime so we have to figure out which one it is.
                if value.tzinfo is None:
                    return DataType.LOCALDATETIME.value
                else:
                    return DataType.DATETIME.value                
            if isinstance(value, WGS84Point):
                return DataType.POINTWGS84.value
            if isinstance(value, CartesianPoint):
                return DataType.POINTCARTESIAN.value
        except:    
            return DataType.UNKNOWN.value

        return DataType.UNKNOWN.value        

    def escapeSingleQuote(self, dataValue):
        return dataValue.replace("'", "\\'")
        
    def escapeDoubleQuote(self, dataValue):
        return dataValue.replace('"', '\\"')  
        
    def genPropEqualTo(self, dataValue=None, neoType = None):
        
        if neoType == DataType.STRING.value:
            setEqualTo = '"{}"'.format(self.escapeDoubleQuote(dataValue))
        elif neoType in (DataType.INT.value,  DataType.FLOAT.value):
            setEqualTo = "{}".format(dataValue)
        elif neoType == DataType.BOOLEAN.value:
            setEqualTo = "toBoolean('{}')".format(dataValue)
        elif neoType == ( DataType.DATE.value):
            setEqualTo = "date('{}')".format(dataValue)        
        elif neoType == ( DataType.DATETIME.value):
            # now generate the correct string representation for the cypher stmt
            setEqualTo = "datetime('{}')".format(dataValue)    
        elif neoType == ( DataType.DURATION.value):
            setEqualTo = "duration('{}')".format(dataValue)            
        elif neoType == ( DataType.TIME.value):
            setEqualTo = "time('{}')".format(dataValue)        
        elif neoType == ( DataType.LOCALTIME.value):
            setEqualTo = "localtime('{}')".format(dataValue)        
        elif neoType == ( DataType.LOCALDATETIME.value):
            setEqualTo = "localdatetime('{}')".format(dataValue)     
        elif neoType == DataType.POINTCARTESIAN.value:
            start = dataValue.find("(")  
            end = dataValue.find(")")
            data = dataValue[start+1:end].strip().split(" ")
            if len(data) > 2:
                setEqualTo = "point({}x:{}, y:{}, z:{}{})".format("{", data[0], data[1], data[2], "}") 
            else:
                setEqualTo = "point({}x:{}, y:{}{})".format("{", data[0], data[1], "}") 
        elif neoType == DataType.POINTWGS84.value:
            start = dataValue.find("(")  
            end = dataValue.find(")")
            data = dataValue[start+1:end].split(" ")
            if len(data) > 2:
                setEqualTo = "point({}longitude:{}, latitude:{}, height:{}{})".format("{", data[0], data[1], data[2], "}") 
            else:
                setEqualTo = "point({}longitude:{}, latitude:{}{})".format("{", data[0], data[1], "}") 
        else:
            setEqualTo = ""
        
        return setEqualTo
        
    def convertTypeToString(self, dataValue):
        '''
        converts a python value of a given datatype to it's string value
        '''
        if isinstance(dataValue, str):
            return dataValue
        elif isinstance(dataValue, bool):
            if dataValue == True:
                return "True"
            else:
                return "False"
        elif isinstance(dataValue, int):
            return str(dataValue)
        elif isinstance(dataValue, float):
            return str(dataValue)    
        elif isinstance(dataValue, Duration):
            return str(dataValue)   
        elif isinstance(dataValue, Time):
            returnStr = dataValue.iso_format()
            return returnStr 
        elif isinstance(dataValue, Date):
            returnStr = "{:0>4}-{:0>2}-{:0>2}".format(dataValue.year, dataValue.month, dataValue.day)
            return returnStr 
        elif isinstance(dataValue, DateTime): #"yyyy-MM-dd hh:mm:ss:zzz"
            returnStr = dataValue.iso_format()
            return returnStr 
        elif isinstance(dataValue, WGS84Point):

            return str(dataValue) 
        elif isinstance(dataValue, CartesianPoint):
            return str(dataValue)      
        else:
            try:
                conversion = str(dataValue)
                return conversion
            except:
                return "unable to convert {} to a string".format(type(dataValue))
        
      
    def castType(self, dataType=None, stringValue=None):
        '''
        this will convert the stringValue value into the appropriate python datatype.
        '''
        try:
            # if the stringValue is already some non-string datatype then just return it
            if not isinstance(stringValue, str):
                return stringValue
            # convert the string data type to the requested dataType
            if dataType == DataType.STRING.value:
                return str(stringValue)
            if dataType == DataType.BOOLEAN.value:
                aBool = bool()
                if stringValue in ("False", "false"):
                    aBool = False
                else:
                    aBool = True
                return aBool
            if dataType == DataType.INT.value:
                return int(stringValue)
            if dataType == DataType.FLOAT.value:
                return float(stringValue)
            if dataType == DataType.POINTWGS84.value:
                # convert stringValue into a tuple for point constructor
                start = stringValue.find("(")  
                end = stringValue.find(")")
                pointData = stringValue[start+1:end].strip().split(" ")
                # return a WGS84Point object
                aPoint = WGS84Point(pointData)
                return aPoint
            if dataType == DataType.POINTCARTESIAN.value:
                # convert stringValue into a tuple for point constructor
                start = stringValue.find("(")  
                end = stringValue.find(")")
                pointData = stringValue[start+1:end].strip().split(" ")
                # return a CartesianPoint object
                aPoint = CartesianPoint(pointData)
                return aPoint
            if dataType == DataType.TIME.value:
                # we assume a valid time syntax was entered in the string, no parsing is attempted
                try:
                    testTime = Time(stringValue)
                    return testTime
                except:
                    return None
            if dataType == DataType.DURATION.value:
                # we assume a valid duration syntax was entered in the string, no parsing is attempted
                try:
                    testDuration = Duration(stringValue)
                    return testDuration
                except:
                    return None
            if dataType == DataType.DATE.value:
                try:
                    testDate = parse(stringValue)
                    return Date(testDate.year, testDate.month, testDate.day)
                except:
                    return None
            if dataType == DataType.DATETIME.value:
                # we assume a valid datetime syntax was entered in the string, no parsing is attempted
                try:
                    testDateTime = DateTime(stringValue)
                    return testDateTime
                except:
                    return None                    

        except:
            return "Error Converting {} to {}".format(stringValue, dataType)
