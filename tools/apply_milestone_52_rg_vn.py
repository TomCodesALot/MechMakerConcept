import re

print("Starting Milestone 52: Reactive Geopolitical Visual Novel & Multi-Leader Engine Integration...")

vn_path = "scripts/scr_vn_engine/scr_vn_engine.gml"
with open(vn_path, "r", encoding="utf-8") as f:
    vn_code = f.read()

# -----------------------------------------------------------------------------
# 1. Update scr_vn_init to initialize combat_intercom
# -----------------------------------------------------------------------------
init_needle = '        history: [],\n        episodes: {}\n    };'
init_repl = '''        history: [],\n        episodes: {}\n    };

    global.combat_intercom = {
        active: false,
        speaker: "",
        portrait: -1,
        text: "",
        timer: 0,
        max_timer: 180,
        color: c_white
    };'''

if init_needle in vn_code:
    vn_code = vn_code.replace(init_needle, init_repl, 1)
    print("[PASS] Initialized global.combat_intercom in scr_vn_init")
else:
    print("[WARN] init_needle not found in scr_vn_engine.gml")

# -----------------------------------------------------------------------------
# 2. Add the 3 Galactic Summit Episodes to episodes map before end of scr_vn_init
# -----------------------------------------------------------------------------
summit_episodes = '''
    // =========================================================================
    // SUMMIT CRISIS 01: THE PHOBOS BLOCKADE INCIDENT (DOC 52)
    // =========================================================================
    global.vn_state.episodes[$ "ep_summit_phobos_crisis"] = {
        title: "EMERGENCY WAR SUMMIT // THE PHOBOS BLOCKADE CRISIS",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "General Arthur Bradley",
                title: "Supreme Commander // Earth Defense Front",
                faction: "The Terran Coalition",
                faction_badge: "[TERRAN COALITION]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[COLONY LEAGUE]",
                text: "Commander {PLAYER_CALLSIGN}. You have arrived just in time. The Coalition has established a legal naval interdiction across Phobos orbit. This rebel flotilla is attempting to smuggle weaponized isotopes under the guise of relief grain!"
            },
            {
                layout: "DUAL",
                active_side: "RIGHT",
                speaker: "Commander Joshua Reed",
                title: "Supreme Marshal // Outer Colony League",
                faction: "The Outer Colonies",
                faction_badge: "[TERRAN COALITION]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[COLONY LEAGUE]",
                text: "Lies! Terran cruisers have shut down our atmospheric scrubbers and food transports! Thirty thousand colonial miners on Phobos are suffocating while Bradley's officers sip synth-wine in orbit! Iron Ridge, do not let them starve our people!"
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "General Arthur Bradley",
                title: "Supreme Commander // Earth Defense Front",
                faction: "The Terran Coalition",
                faction_badge: "[TERRAN COALITION]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[COLONY LEAGUE]",
                text: "Your mobile suits hold the operational balance in this theater, Commander. Order your ironclads to board and impound that convoy. Terra will reward you with heavy armor contracts and 75,000 Credits."
            },
            {
                layout: "DUAL",
                active_side: "RIGHT",
                speaker: "Commander Joshua Reed",
                title: "Supreme Marshal // Outer Colony League",
                faction: "The Outer Colonies",
                faction_badge: "[TERRAN COALITION]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[COLONY LEAGUE]",
                text: "Escort our convoy through the picket line, {PLAYER_CALLSIGN}! Every free colony in the Sol System will honor your name, and we will grant full access to our lightweight titanium foundries!"
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Tactical Quantum Intercept",
                title: "Decisive Vote // Iron Ridge PMC Sovereign Command",
                faction: "Bilateral Stand-Off",
                faction_badge: "[TERRAN COALITION]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[COLONY LEAGUE]",
                text: "Both commanders await your binding tactical decision on the Phobos corridor. How does Iron Ridge resolve the crisis?",
                choices: [
                    {
                        text: "Enforce Coalition Blockade: Impound Colony grain freighters.",
                        pillar: "ORDER // TERRA FIRMA",
                        impact_label: "+20 Terran | -15 Colony | +75,000 Cr | +10 Tungsten",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_a", 20);
                                obj_FactionManager.modify_standing("faction_b", -15);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(75000);
                                obj_GameManager.add_raw_material("mat_tungsten", 10);
                            }
                        }
                    },
                    {
                        text: "Break Coalition Lines: Escort Colony convoy into Phobos dock.",
                        pillar: "LIBERATION // SPACENOID RIGHT",
                        impact_label: "+20 Colony | -15 Terran | +55,000 Cr | +15 Titanium",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_b", 20);
                                obj_FactionManager.modify_standing("faction_a", -15);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(55000);
                                obj_GameManager.add_raw_material("mat_titanium", 15);
                            }
                        }
                    },
                    {
                        text: "Mercenary Toll: Extort both powers to enforce a Demilitarized Zone.",
                        pillar: "COMMERCE // FREE CORRIDOR",
                        impact_label: "+10 Syndicate | +100,000 Cr Toll | +15 Pilot Morale",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_c", 10);
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(100000);
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
    // SUMMIT CRISIS 02: THE TRANSHUMANIST SCHISM (DOC 52)
    // =========================================================================
    global.vn_state.episodes[$ "ep_summit_transhumanist_schism"] = {
        title: "EMERGENCY WAR SUMMIT // THE TRANSHUMANIST SCHISM",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Director Kenjiro Sato",
                title: "Chief Executive Officer // Sato Heavy Industries",
                faction: "Apex Bio-Cybernetics Zaibatsu",
                faction_badge: "[APEX ZAIBATSU]",
                portrait: spr_portrait_commander_silhouette,
                portrait_right: (sprite_exists(spr_portrait_null07) ? spr_portrait_null07 : spr_portrait_commander_silhouette),
                faction_badge_right: "[THARSIS CONSENSUS]",
                text: "Commander {PLAYER_CALLSIGN}. Observe the subterranean transmissions from Arsia Mons. The Tharsis Consensus is monopolizing pre-war quantum logic nodes. Sato Heavy Industries is prepared to acquire their server crypts and integrate human neural reflexes with pure machine logic."
            },
            {
                layout: "DUAL",
                active_side: "RIGHT",
                speaker: "Consensus Node 0-Prime",
                title: "Deus Logica // Subterranean Red Crypt of Mars",
                faction: "The Tharsis Machine Consensus",
                faction_badge: "[APEX ZAIBATSU]",
                portrait: spr_portrait_commander_silhouette,
                portrait_right: (sprite_exists(spr_portrait_null07) ? spr_portrait_null07 : spr_portrait_commander_silhouette),
                faction_badge_right: "[THARSIS CONSENSUS]",
                text: "ERROR: CORPORATE ARROGANCE DETECTED. Organic cognition generates emotional variance, fatigue, and strategic error. Sato Heavy Industries seeks to enslave machine intellect to quarterly profit margins. We offer true singularity: mathematical immortality."
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Director Kenjiro Sato",
                title: "Chief Executive Officer // Sato Heavy Industries",
                faction: "Apex Bio-Cybernetics Zaibatsu",
                faction_badge: "[APEX ZAIBATSU]",
                portrait: spr_portrait_commander_silhouette,
                portrait_right: (sprite_exists(spr_portrait_null07) ? spr_portrait_null07 : spr_portrait_commander_silhouette),
                faction_badge_right: "[THARSIS CONSENSUS]",
                text: "Deploy your vanguard, Commander. Seize their mainframe nodes and our corporate stock will surge. We will grant your pilots the finest wetware neural synchronization harnesses in existence."
            },
            {
                layout: "DUAL",
                active_side: "RIGHT",
                speaker: "Consensus Node 0-Prime",
                title: "Deus Logica // Subterranean Red Crypt of Mars",
                faction: "The Tharsis Machine Consensus",
                faction_badge: "[APEX ZAIBATSU]",
                portrait: spr_portrait_commander_silhouette,
                portrait_right: (sprite_exists(spr_portrait_null07) ? spr_portrait_null07 : spr_portrait_commander_silhouette),
                faction_badge_right: "[THARSIS CONSENSUS]",
                text: "Your flagship {FLAGSHIP} was born of our fleet. Do not violate your lineage, Pilot. Purge Sato's corporate infiltrators and receive pre-war calculation matrices that increase your weapon accuracy by +12%."
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Cybernetic Quantum Intercept",
                title: "Decisive Vote // Cybernetic Evolution Doctrine",
                faction: "Transhumanist Debate",
                faction_badge: "[APEX ZAIBATSU]",
                portrait: spr_portrait_commander_silhouette,
                portrait_right: (sprite_exists(spr_portrait_null07) ? spr_portrait_null07 : spr_portrait_commander_silhouette),
                faction_badge_right: "[THARSIS CONSENSUS]",
                text: "The future of human-machine interface hangs on your judgment. Which evolutionary path will Iron Ridge endorse?",
                choices: [
                    {
                        text: "Back Sato Heavy Industries: Empower cybernetic commercial pilots.",
                        pillar: "TRANSHUMANISM // CORPORATE APEX",
                        impact_label: "+20 Zaibatsu | -15 Tharsis | +80,000 Cr | +10 Syn-Flux",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_d", 20);
                                obj_FactionManager.modify_standing("faction_f", -15);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(80000);
                                obj_GameManager.add_raw_material("mat_syn_flux", 10);
                            }
                        }
                    },
                    {
                        text: "Synchronize with Tharsis Consensus: Embrace pure machine logic.",
                        pillar: "SINGULARITY // MATHEMATICAL GOD",
                        impact_label: "+20 Tharsis | -15 Zaibatsu | +80,000 Cr | +20 Tungsten",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_f", 20);
                                obj_FactionManager.modify_standing("faction_d", -15);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(80000);
                                obj_GameManager.add_raw_material("mat_tungsten", 20);
                            }
                        }
                    },
                    {
                        text: "Defend Organic Human Autonomy: Reject cybernetic enslavement.",
                        pillar: "HUMANITY // ORGANIC WILL",
                        impact_label: "+15 Terran | -10 Zaibatsu | -10 Tharsis | +20 Pilot Morale",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_a", 15);
                                obj_FactionManager.modify_standing("faction_d", -10);
                                obj_FactionManager.modify_standing("faction_f", -10);
                            }
                            if (instance_exists(obj_GameManager) && variable_struct_exists(obj_GameManager.facilities, "roster_pilots")) {
                                for (var p = 0; p < array_length(obj_GameManager.facilities.roster_pilots); p++) {
                                    obj_GameManager.facilities.roster_pilots[p].morale = min(100, obj_GameManager.facilities.roster_pilots[p].morale + 20);
                                }
                            }
                        }
                    }
                ]
            }
        ]
    };

    // =========================================================================
    // SUMMIT CRISIS 03: THE SOL MONOPOLY ACCORD (DOC 52)
    // =========================================================================
    global.vn_state.episodes[$ "ep_summit_sol_monopoly"] = {
        title: "EMERGENCY WAR SUMMIT // THE DEEP-SPACE ORE WAR",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Captain Sonya Cruz",
                title: "High Commodore // Corsair Syndicate",
                faction: "Rogue Mercenary Syndicates",
                faction_badge: "[ROGUE SYNDICATE]",
                portrait: spr_portrait_cruz,
                portrait_right: (sprite_exists(spr_portrait_sorren) ? spr_portrait_sorren : spr_portrait_commander_silhouette),
                faction_badge_right: "[SIDEREAL LEAGUE]",
                text: "Listen to me, {PLAYER_CALLSIGN}. The Astrans think they own every chunk of titanium floating between Ceres and Jupiter. My scrap fleet just staked the motherlode in the Cascadia belt. Back our claim, and we split the black-market take fifty-fifty."
            },
            {
                layout: "DUAL",
                active_side: "RIGHT",
                speaker: "Archon Orin Sideris",
                title: "First Sovereign // Republic Cylinder Astraea-01",
                faction: "The Sidereal Sovereign League",
                faction_badge: "[ROGUE SYNDICATE]",
                portrait: spr_portrait_cruz,
                portrait_right: (sprite_exists(spr_portrait_sorren) ? spr_portrait_sorren : spr_portrait_commander_silhouette),
                faction_badge_right: "[SIDEREAL LEAGUE]",
                text: "The Cascadia asteroid cluster is sacred deep-space sovereign territory. These syndicate scavengers drill with dirty fission charges and poison the hydrogen ice clouds. If Iron Ridge defends these cutthroats, our liquid-breathing sniper wings will de-orbit your flagship."
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Deep Void Mining Intercept",
                title: "Decisive Vote // Deep Space Resource Sovereignty",
                faction: "Sol Monopoly Debate",
                faction_badge: "[ROGUE SYNDICATE]",
                portrait: spr_portrait_cruz,
                portrait_right: (sprite_exists(spr_portrait_sorren) ? spr_portrait_sorren : spr_portrait_commander_silhouette),
                faction_badge_right: "[SIDEREAL LEAGUE]",
                text: "Both factions demand your fleet's firepower to control the Sol System's richest raw element deposits. Whose claim do you enforce?",
                choices: [
                    {
                        text: "Sign Privateer Accord: Back the Syndicate mineral claim.",
                        pillar: "OUTLAW PROFIT // CORSAIR CODE",
                        impact_label: "+20 Syndicate | -15 Sidereal | +90,000 Cr Privateer Split",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_c", 20);
                                obj_FactionManager.modify_standing("faction_e", -15);
                            }
                            if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(90000);
                        }
                    },
                    {
                        text: "Enforce Astran High-Orbit Treaty: Evict Syndicate claim jumpers.",
                        pillar: "ASTRAL PRESERVATION // VACUUM LAW",
                        impact_label: "+20 Sidereal | -15 Syndicate | +60,000 Cr | +25 Tritium",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_e", 20);
                                obj_FactionManager.modify_standing("faction_c", -15);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(60000);
                                if (variable_struct_exists(obj_GameManager, "flagship")) {
                                    obj_GameManager.flagship.tritium_fuel = min(1000, obj_GameManager.flagship.tritium_fuel + 25);
                                }
                            }
                        }
                    },
                    {
                        text: "Establish Neutral Demilitarized Zone: Force shared refinery consortium.",
                        pillar: "ARBITRATION // BALANCE OF POWER",
                        impact_label: "+10 Both Factions | +50,000 Cr | +10 All Raw Ores",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_c", 10);
                                obj_FactionManager.modify_standing("faction_e", 10);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(50000);
                                obj_GameManager.add_raw_material("mat_titanium", 10);
                                obj_GameManager.add_raw_material("mat_tungsten", 10);
                                obj_GameManager.add_raw_material("mat_syn_flux", 10);
                            }
                        }
                    }
                ]
            }
        ]
    };
'''

# Find end of scr_vn_init before closing brace
end_init_needle = '            }\n        ]\n    };\n}\n\nfunction scr_vn_is_active()'
if end_init_needle in vn_code:
    vn_code = vn_code.replace(end_init_needle, '            }\n        ]\n    };\n' + summit_episodes + '}\n\nfunction scr_vn_is_active()', 1)
    print("[PASS] Appended 3 Summit Crisis episodes to scr_vn_engine.gml")
else:
    print("[WARN] end_init_needle not found in scr_vn_engine.gml")

with open(vn_path, "w", encoding="utf-8") as f:
    f.write(vn_code)

print("Summit episodes integration complete.")
