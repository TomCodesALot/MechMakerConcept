import re

print("Starting Milestone 51 Final Phases Integration...")

# =============================================================================
# 1. UPDATE SCRIPTS/SCR_VN_ENGINE/SCR_VN_ENGINE.GML
# =============================================================================
vn_path = "scripts/scr_vn_engine/scr_vn_engine.gml"
with open(vn_path, "r", encoding="utf-8") as f:
    vn_content = f.read()

episodes_to_add = '''
    // =========================================================================
    // EPISODE AUDIENCE: THE SIDEREAL SOVEREIGN LEAGUE (DOC 37 & DOC 51)
    // =========================================================================
    global.vn_state.episodes[$ "ep_audience_sidereal"] = {
        title: "WAR ROOM QUANTUM LINK // ARCHON ORIN SIDERIS",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                speaker: "Archon Orin Sideris",
                title: "First Sovereign // Republic Cylinder Astraea-01",
                faction: "The Sidereal Sovereign League",
                faction_badge: "[SIDEREAL LEAGUE]",
                portrait: (sprite_exists(spr_portrait_sorren) ? spr_portrait_sorren : spr_portrait_commander_silhouette),
                text: "Greetings across the void, Commander. We observe your foundry's works from the Trojan Lagrange clusters. Terrestrial humanity clings to a dying gravity well, while my people have breathed liquid fluorocarbon and survived four generations in the eternal dark. Ally with Astraea, and you shall claim the true future beyond the cradle.",
                choices: [
                    {
                        text: "Iron Ridge pledges solidarity to the Astran Spacenoid republic.",
                        pillar: "ASTRAL SOVEREIGNTY // BEYOND THE CRADLE",
                        impact_label: "+15 Sidereal | -10 Terran | +45,000 Cr | +20 Tritium",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_e", 15);
                                obj_FactionManager.modify_standing("faction_a", -10);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(45000);
                                if (variable_struct_exists(obj_GameManager, "flagship")) {
                                    obj_GameManager.flagship.tritium_fuel = min(1000, obj_GameManager.flagship.tritium_fuel + 20);
                                }
                            }
                        }
                    },
                    {
                        text: "We propose a reciprocal exchange of advanced superconductor metallurgy.",
                        pillar: "METALLURGICAL SYMBIOSIS // SUPERCONDUCTORS",
                        impact_label: "+10 Sidereal | +15x Titanium | +10x Syn-Flux Crystals",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_e", 10);
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_raw_material("mat_titanium", 15);
                                obj_GameManager.add_raw_material("mat_syn_flux", 10);
                            }
                        }
                    },
                    {
                        text: "Abandoning Earth is treason to human history. We reject your isolationism.",
                        pillar: "TERRESTRIAL DEFENSE // GRAVITY WELL COVENANT",
                        impact_label: "-12 Sidereal | +12 Terran Standing",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_e", -12);
                                obj_FactionManager.modify_standing("faction_a", 12);
                            }
                        }
                    }
                ]
            }
        ]
    };

    // =========================================================================
    // EPISODE AUDIENCE: THE THARSIS MACHINE CONSENSUS (DOC 37 & DOC 51)
    // =========================================================================
    global.vn_state.episodes[$ "ep_audience_tharsis"] = {
        title: "SUBSURFACE TRANSMISSION // CONSENSUS NODE 0-PRIME",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                speaker: "Consensus Node 0-Prime",
                title: "Deus Logica // Subterranean Red Crypt of Mars",
                faction: "The Tharsis Machine Consensus",
                faction_badge: "[THARSIS CONSENSUS]",
                portrait: (sprite_exists(spr_portrait_null07) ? spr_portrait_null07 : spr_portrait_commander_silhouette),
                text: "TELEMETRY LOCK CONFIRMED. Acoustic harmonic matches First Mars Colonization Fleet Vessel 07: APV Hephaestus. Query: How does an organic salvage unit command our lost crucible carrier? We are the survivors of the Red Crypt. Surrender your combat computation to the Consensus, and achieve 99.87% battlefield survival.",
                choices: [
                    {
                        text: "Synchronize Hephaestus compute core with Tharsis quantum calculation.",
                        pillar: "ALGORITHMIC HARMONY // PRE-WAR REUNION",
                        impact_label: "+15 Tharsis | +10% Prototyping Precision | +60,000 Cr Compute Grant",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_f", 15);
                            if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(60000);
                        }
                    },
                    {
                        text: "We trade raw Martian ore extractions for tactical cybernetic schematics.",
                        pillar: "TACTICAL EXPLOITATION // SUBTERRANEAN TRADE",
                        impact_label: "+8 Tharsis | +20x Tungsten | +15x Titanium Ores",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_f", 8);
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_raw_material("mat_tungsten", 20);
                                obj_GameManager.add_raw_material("mat_titanium", 15);
                            }
                        }
                    },
                    {
                        text: "The Hephaestus is an independent PMC vessel. We will never submit to machine rule.",
                        pillar: "ORGANIC AUTONOMY // WILL OF FLESH",
                        impact_label: "-12 Tharsis | +15 Pilot Morale | +5 Terran Standing",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_f", -12);
                                obj_FactionManager.modify_standing("faction_a", 5);
                            }
                            if (instance_exists(obj_GameManager) && variable_struct_exists(obj_GameManager, "facilities")) {
                                if (variable_struct_exists(obj_GameManager.facilities, "roster_pilots")) {
                                    for (var p = 0; p < array_length(obj_GameManager.facilities.roster_pilots); p++) {
                                        obj_GameManager.facilities.roster_pilots[p].morale = min(100, obj_GameManager.facilities.roster_pilots[p].morale + 15);
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        ]
    };

    // =========================================================================
    // EPISODE 02: SHADOWS OVER MARS (STRATEGIC CAMPAIGN MILESTONE)
    // =========================================================================
    global.vn_state.episodes[$ "ep_02_shadows_over_mars"] = {
        title: "STRATEGIC DISPATCH // THE RED REDOUBT ESCALATION",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                speaker: "Lt. Vance",
                title: "Tactical Executive Officer // USN-X Hephaestus",
                faction: "Iron Ridge PMC",
                faction_badge: "[VANGUARD SEC]",
                portrait: (sprite_exists(spr_portrait_vance) ? spr_portrait_vance : spr_portrait_commander_male),
                text: "Commander, long-range planetary sensors indicate full mobilization across the Martian perimeter. The Terran Coalition and the Outer Colonies have established fortified strongholds in the equatorial canyons. If we move in now, our Mobile Suits can claim high-value mining redoubts."
            },
            {
                speaker: "Chief Logistics Officer Kovacs",
                title: "Foundry Operations // Hephaestus Deck 3",
                faction: "Iron Ridge PMC",
                faction_badge: "[LOGISTICS]",
                portrait: (sprite_exists(spr_portrait_cruz) ? spr_portrait_cruz : spr_portrait_commander_female),
                text: "Our sintering crucible is primed for heavy composite production. Sintering high-density alloys now will give our platoon the armor needed to breach Martian bunker networks.",
                choices: [
                    {
                        text: "Authorize planetary strike readiness. Target Martian mineral zones.",
                        pillar: "OFFENSIVE STRIKE // PLANETARY EXPANSION",
                        impact_label: "+10 Pilot Morale | +35,000 Cr Operational Retainer",
                        action: function() {
                            if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(35000);
                        }
                    },
                    {
                        text: "Consolidate our supply lines first. Upgrade the Hephaestus foundry.",
                        pillar: "DEFENSIVE FORTIFICATION // INDUSTRIAL CAUTION",
                        impact_label: "+25x Titanium Ore | +15x Tungsten Ingot Stock",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_raw_material("mat_titanium", 25);
                                obj_GameManager.add_raw_material("mat_tungsten", 15);
                            }
                        }
                    }
                ]
            }
        ]
    };
'''

# Find the end of ep_audience_zaibatsu and insert
target_needle = '            }\n        ]\n    };\n}\n\nfunction scr_vn_is_active()'
if target_needle in vn_content:
    replacement = '            }\n        ]\n    };\n' + episodes_to_add + '}\n\nfunction scr_vn_is_active()'
    vn_content = vn_content.replace(target_needle, replacement, 1)
    with open(vn_path, "w", encoding="utf-8") as f:
        f.write(vn_content)
    print("[SUCCESS] Appended Sidereal, Tharsis, and Episode 02 to scr_vn_engine.gml")
else:
    print("[ERROR] Could not find target needle in scr_vn_engine.gml")

