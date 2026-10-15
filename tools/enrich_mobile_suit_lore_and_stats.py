#!/usr/bin/env python3
"""
enrich_mobile_suit_lore_and_stats.py
Author: Lore & Worldbuilding Team + GameMaker Coder
Enriches all 100 mobile suits in mobile_suit_catalog.json with:
1. Deep military sci-fi historical development lore.
2. Manufacturing quirks and maintenance complaints.
3. Frontline pilot slang and battlefield reputation.
4. Global production numbers, active counts, casualty counts, kill counts, loss ratios.
5. Dynamic playthrough chronicle logs and initial adoption statuses.
"""

import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT_PATHS = [
    os.path.join(BASE_DIR, "datafiles/mobile_suits/mobile_suit_catalog.json"),
    os.path.join(BASE_DIR, "datafiles/mobile_suit_catalog.json")
]

with open(CAT_PATHS[0], "r", encoding="utf-8") as f:
    catalog = json.load(f)

print(f"Loaded catalog with {len(catalog)} mobile suits.")
