with open('/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_unit_sprites_review.md', 'r') as f:
    text = f.read()

# Add new carousel slides at the top carousel
old_carousel_start = "````carousel\n![1. Tactical Order Dispatch Mode"
new_carousel_slides = """````carousel
![1. Tactical Directive Modal — Dual Choice: Auto-Dispatch vs Manual Tactical Sortie](/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/live_directive_modal_dual_choice.png)
<!-- slide -->
![2. Tactical Battle Arena (rm_combat) — Context-Sensitive Sector Biome & Defending Faction OPFOR](/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/live_tactical_arena_sector_integration.png)
<!-- slide -->
![3. Tactical Order Dispatch Mode"""

text = text.replace(old_carousel_start, new_carousel_slides, 1)

# Add section on Tactical Sortie Pipeline
sortie_section = """
---

## 4. Strategic Map to Tactical Combat Sortie Pipeline (`rm_combat`)

The bridge between the macro-scale **Strategic War Map** and the turn-based **Isometric Tactical Combat Arena** is fully operational:

1. **Context-Sensitive Sortie Routing**:
   * When launching an invasion or defensive sortie, `obj_GameManager.active_combat_context` captures the target territory's `sector_id`, `name`, `region`, `controlling_faction`, `defense_rating`, and `garrison_unit`.
2. **Biome & Arena Mapping (`scr_territory_get_battle_map_id`)**:
   * Each of the 33 Sol strategic territories maps directly to an authentic 20×20 isometric battlefield arena (e.g., Aethelgard Prime -> Colony Shell, Granite Redoubt -> Amazon Jungle Delta, Tartarus -> Hollowed Asteroid Bastion, Olympus Mons -> Volcanic Caldera Ridge).
3. **Defending OPFOR Customization**:
   * Opponent battlegroups spawn color-coded in their faction theme (Terran Blue, Colony Teal, Syndicate Orange, Zaibatsu Violet, Sidereal Indigo, Mars Red) with matching unit callsigns and garrison boss commanders.
4. **Player Hangar Deployment**:
   * Deployable custom mobile suits assembled in the Factory Hangar automatically replace generic units with their custom names, armor ratings, and pilot assignments.
5. **After-Action Territory Conquest (AAR)**:
   * Achieving victory in `rm_combat` immediately claims the sector for Iron Ridge PMC, recalculates galactic hegemony parity, deposits bounty credits and salvage ingots, and returns to the War Map with a victory salute toast!
"""

insert_pos = text.find("## 4. Verification & Validation Summary")
text = text[:insert_pos] + sortie_section + "\n" + text[insert_pos:]

with open('/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_unit_sprites_review.md', 'w') as f:
    f.write(text)

print("Updated tactical_unit_sprites_review.md with Tactical Sortie Pipeline documentation.")
