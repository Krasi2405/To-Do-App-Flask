#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/To-Do-App-Flask")

from app import app as application
application.secret_key = "ofsajpiofjeiwjg09w0ejgfajodf9hew809g092uja012-$90ash"
