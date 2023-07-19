"""
Module containing all HTTP related classes

Use this module (instead of the more specific ones) when importing Headers,
Request and Response outside this module.
"""

from frapy.http.headers import Headers
from frapy.http.request import Request
from frapy.http.request.form import FormRequest
from frapy.http.request.json_request import JsonRequest
from frapy.http.request.rpc import XmlRpcRequest
from frapy.http.response import Response
from frapy.http.response.html import HtmlResponse
from frapy.http.response.text import TextResponse
from frapy.http.response.xml import XmlResponse
