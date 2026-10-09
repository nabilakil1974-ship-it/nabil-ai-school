#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NABIL AI thin lesson-factory entrypoint.

NABIL_THIN_FACTORY_ENTRYPOINT
All implementation lives under scripts/nabil_factory/.
"""
from scripts.nabil_factory.factory import orchestrator as _orchestrator

globals().update(_orchestrator.export_symbols())

if __name__ == "__main__":
    raise SystemExit(_orchestrator._cli_entry())
