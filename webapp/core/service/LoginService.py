"""
    LoginService
"""

from webapp.core.service import LoginServiceImpl as impl


def userCheckMl(params):
    return impl.userCheckMl(params)


def select_golden_zone(params):
    return impl.select_golden_zone(params)