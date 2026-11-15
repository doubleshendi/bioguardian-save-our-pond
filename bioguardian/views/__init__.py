"""Views package for BioGuardian screens."""

from bioguardian.views.s01_welcome import render_s01_welcome
from bioguardian.views.s02_setup import render_s02_setup
from bioguardian.views.s03_instructions import render_s03_instructions
from bioguardian.views.s04_dashboard import render_s04_dashboard
from bioguardian.views.s05_predict import render_s05_predict
from bioguardian.views.s06_action import render_s06_action
from bioguardian.views.s07_learn import render_s07_learn
from bioguardian.views.s08_restore import render_s08_restore
from bioguardian.views.s09_round_result import render_s09_round_result
from bioguardian.views.s10_final_report import render_s10_final_report
from bioguardian.views.s11_help import render_s11_help

__all__ = [
    "render_s01_welcome",
    "render_s02_setup",
    "render_s03_instructions",
    "render_s04_dashboard",
    "render_s05_predict",
    "render_s06_action",
    "render_s07_learn",
    "render_s08_restore",
    "render_s09_round_result",
    "render_s10_final_report",
    "render_s11_help"
]
