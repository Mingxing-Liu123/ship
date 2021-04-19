# -*-coding:utf-8-*-
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
