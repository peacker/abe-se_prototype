#!/usr/bin/python

from subprocess import call

call( ["python", "SET_AUTHORITY_server.py"] )
call( ["python", "SET_VPSS_client.py"] )
call( ["python", "SET_SEARCH_server.py"] )
call( ["python", "SET_CLOUD_server.py"] )

"""
execfile( "SET_AUTHORITY_server.py" )
execfile( "SET_VPSS_client.py" )
execfile( "SET_SEARCH_server.py" )
execfile( "SET_CLOUD_server.py" )

import SET_AUTHORITY_server
import SET_VPSS_client
import SET_SEARCH_server
import SET_CLOUD_server
"""
