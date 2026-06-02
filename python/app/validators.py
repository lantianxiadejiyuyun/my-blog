# ============================================================
# app/validators.py — 请求参数校验
# ============================================================
from functools import wraps
from flask import request
from .response import fail

