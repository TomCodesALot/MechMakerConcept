/// @desc Retro 16-Bit Visual Novel War Room Episode Engine (Doc 51)
/// Handles narrative episodes, faction leader audiences, and Tri-Pillar consequential agency.

function scr_vn_init() {
    global.vn_state = {
        active: false,
        episode_id: "",
        step_idx: 0,
        char_progress: 0,
        typewriter_speed: 1.2,
        last_tick_char: 0,
        history: [],
        episodes: {}
    };

    global.combat_intercom = {
        active: false,
        speaker: "",
        portrait: -1,
        text: "",
        timer: 0,
        max_timer: 180,
        color: c_white
    };

    // =========================================================================
    // EPISODE 00-A: CABIN DISCOVERY // CASCADIA GRAVEYARD
    // =========================================================================
    global.vn_state.episodes[$ "ep_00_cabin_discovery"] = {
        title: "LOGBOOK // CASCADIA ASTEROID GRAVEYARD (YEAR 215)",
        bg_scene: spr_loc_hangar_bay,
        nodes: [
            {
                speaker: "Cockpit Life Support",
                title: "Scrap Tug 'Rust-Bucket' // Cabin Environment",
                faction: "Void Salvager",
                faction_badge: "[SCRAP TUG]",
                portrait: spr_portrait_commander_silhouette,
                text: "Deep asteroid graveyard. Cabin temperature: 4 degrees Celsius. Oxygen scrubbers at 38%. The loan-shark countdown beacon on Ceres has barely 72 hours left before they repossess my life support... and then radar catches an impossible return in the ice belt."
            },
            {
                speaker: "Viewport Optic Scanner",
                title: "Visual Telemetry // USN-X Hephaestus",
                faction: "Pre-War Derelict",
                faction_badge: "[DREADNOUGHT]",
                portrait: spr_portrait_commander_silhouette,
                text: "Through the pitted glass, the colossal silhouette of a pre-war dreadnought drifts through the asteroid shadows. Five hundred meters of reinforced armor plating, dark and dead in the water. A faint high-frequency military beacon pulses from its dorsal tower: SOS-EMERGENCY-SEC-00."
            },
            {
                speaker: "Personal Logbook PDA",
                title: "Salvager Ledger Rev 4.12 // Pre-EVA Check",
                faction: "Personal Dossier",
                faction_badge: "[LOGBOOK ENTRY]",
                portrait: spr_portrait_commander_silhouette,
                text: "Before firing thrusters and burning toward that unsealed hangar airlock, I bring up my personal logbook. Who was I before I ended up scavenging scrap on the edge of nothingness?",
                choices: [
                    {
                        text: "Access Cockpit Ledger and review pilot background & traits.",
                        pillar: "LOGBOOK ACCESS // PILOT DOSSIER",
                        impact_label: "[OPEN QUESTIONNAIRE]",
                        action: function() {
                            if (instance_exists(obj_HQTerminal)) {
                                obj_HQTerminal.intro_page = 1;
                                obj_HQTerminal.q_step = 0;
                            }
                        }
                    }
                ]
            }
        ]
    };

    // =========================================================================
    // EPISODE 00-B: PIRATE DECOY TRAP & PROTOTYPE AWAKENING
    // =========================================================================
    global.vn_state.episodes[$ "ep_00_pirate_trap"] = {
        title: "RED ALERT // PIRATE DECOY TRAP & AIRLOCK BREACH",
        bg_scene: spr_loc_hangar_bay,
        nodes: [
            {
                speaker: "Cockpit Threat Radar",
                title: "CAS-RADAR-LOCK // DECOY IDENTIFIED",
                faction: "Void Reavers",
                faction_badge: "[AMBUSH DETECTED]",
                portrait: spr_portrait_commander_silhouette,
                text: "WARNING! The distress ping was an encrypted lure! Three armed bandit signatures dropped out of the asteroid shadows on attack vector! Corsair strike craft firing kinetic rounds!"
            },
            {
                speaker: "Pirate Intercept Channel",
                title: "Corsair Lead Gunship // Intercept Flight",
                faction: "Hyena Pack",
                faction_badge: "[HYENA RAIDERS]",
                portrait: spr_portrait_commander_male,
                text: "'Look at that little scrap cockroach darting for the airlock! Sever their thrusters! That pre-war dreadnought belongs to the Hyena pack!'"
            },
            {
                speaker: "Airlock Blast Tannoy",
                title: "USN-X Hephaestus // Emergency Docking Bay 1",
                faction: "Flagship Vault",
                faction_badge: "[FLAGSHIP VAULT]",
                portrait: spr_portrait_cruz,
                text: "Your scrap skiff slams into the emergency docking bay as autocannon fire chews through the outer threshold. Blast doors slam shut. Emergency red strobes bathe the cavernous hangar in crimson light."
            },
            {
                speaker: "PROMETHEUS-NULL",
                title: "Corrupted Flagship Tactical AI // USN-X Hephaestus",
                faction: "Tactical Core",
                faction_badge: "[FLAGSHIP CORE]",
                portrait: spr_portrait_cruz,
                text: "[CRITICAL MEMORY FAULT: 42 SECTORS CORRUPTED] Biometric scan completed... Organic salvager detected. Threat assessment: 3 raider craft attempting to breach the outer blast door. All original Navy personnel deceased. Wartime continuity dictates emergency command assignment."
            },
            {
                speaker: "PROMETHEUS-NULL",
                title: "Central Fabrication Cradle // Bay 1",
                faction: "Tactical Core",
                faction_badge: "[FLAGSHIP CORE]",
                portrait: spr_portrait_cruz,
                text: "Hydraulic gantry clamps disengage with a deafening hiss of nitrogen gas. Resting in the cradle is a towering, sealed war machine: The GHA-00 Genesis Prototype. The historic first Mobile Suit ever constructed. Neural cockpit link initialized."
            },
            {
                speaker: "PROMETHEUS-NULL",
                title: "Sortie Authorization // Threshold Defense",
                faction: "Tactical Core",
                faction_badge: "[SORTIE LAUNCH]",
                portrait: spr_portrait_cruz,
                text: "Take the helm, Acting Pilot. Sortie through the hangar threshold and neutralize the raider vessels before they breach the ship's reactor bulkheads!",
                choices: [
                    {
                        text: "Engage neural link, power up GHA-00 Prototype, and sortie!",
                        pillar: "SORTIE // DAWN OF THE MOBILE SUIT",
                        impact_label: "[LAUNCH COMBAT]",
                        action: function() {
                            if (instance_exists(obj_HQTerminal)) {
                                obj_HQTerminal.intro_active = false;
                                obj_HQTerminal.show_commander_modal = false;
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.prologue_active = true;
                                obj_GameManager.has_completed_dossier = true;
                            }
                            room_goto(rm_combat);
                        }
                    }
                ]
            }
        ]
    };

    // =========================================================================
    // EPISODE 01: TRI-FACTION INTERCEPT // THE FIRST STRATEGIC RPG CHOICE
    // =========================================================================
    global.vn_state.episodes[$ "ep_01_inauguration"] = {
        title: "EPISODE 01 // TRI-FACTION QUANTUM INTERCEPT",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                speaker: "PROMETHEUS-NULL",
                title: "Tactical Core // USN-X Hephaestus",
                faction: "Flagship AI",
                faction_badge: "[FLAGSHIP CORE]",
                portrait: spr_portrait_cruz,
                text: "Tactical telemetry recorded. All 3 pirate raider craft completely obliterated. Combat analysis: Mobile Suit combat performance exceeds all conventional military craft by an order of magnitude. The Genesis Prototype is fully operational."
            },
            {
                speaker: "PROMETHEUS-NULL",
                title: "Quantum Communications Alert",
                faction: "Flagship AI",
                faction_badge: "[FLAGSHIP CORE]",
                portrait: spr_portrait_cruz,
                text: "CRITICAL BROADCAST DETECTED: The massive energy discharge from the prototype's generator has rippled across the entire Sol System. Three high-priority transmissions from the belligerent solar powers are jamming our quantum receiver simultaneously."
            },
            {
                speaker: "Colonel Gregory Vance",
                title: "Military District 4 // Earth Defense Force",
                faction: "The Terran Coalition",
                faction_badge: "[TERRAN COALITION]",
                portrait: spr_portrait_commander_male,
                text: "Unregistered pilot! That humanoid machine you deployed violates twenty different interplanetary weapons bans, but my tacticians are already calling it the dawn of a new era. Surrender the prototype under emergency jurisdiction, and we will grant your outfit full Federation mercenary accreditation and 60,000 Credits."
            },
            {
                speaker: "Director Kazuki Thorne",
                title: "Executive Board of Directors // Cybernetics Division",
                faction: "Apex Zaibatsu Conglomerate",
                faction_badge: "[APEX ZAIBATSU]",
                portrait: spr_portrait_commander_silhouette,
                text: "Spare us the imperial military posturing, Colonel. Scrapper, the Zaibatsu does not deal in empty oaths. We offer state-of-the-art crucible technology and advanced composite alloys. Transmit your telemetry schematics, and our foundries will supply you with proprietary alloy stock."
            },
            {
                speaker: "Commander Valeria Reyes",
                title: "High Fleet Flagship Vanguard // Jovian Front",
                faction: "Outer Colony League",
                faction_badge: "[JOVIAN COALITION]",
                portrait: spr_portrait_commander_female,
                text: "Do not sell your soul to Earth's tyrants or corporate leeches, salvager! You pulled that machine from the rust with your own blood. The Outer Colonies recognize your sovereign right to salvage. Ally with our liberation front, and our orbital refineries will keep you supplied with raw titanium."
            },
            {
                speaker: "PROMETHEUS-NULL",
                title: "Tactical Core // USN-X Hephaestus",
                faction: "Flagship AI",
                faction_badge: "[FLAGSHIP CORE]",
                portrait: spr_portrait_cruz,
                text: "Directive query: The Hephaestus cannot withstand a coordinated multi-fleet assault. We must register as an independent Private Military Company to bypass maritime embargoes. How do you respond to the emissaries?",
                choices: [
                    {
                        text: "'We will take Federation coin, Colonel Vance.'",
                        pillar: "ORDER // TERRAN ACCREDITATION",
                        impact_label: "+15 Terran | +60,000 Credits | Earth Access",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_a", 15);
                                obj_FactionManager.modify_standing("faction_b", -10);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(60000);
                                if (!variable_struct_exists(obj_GameManager, "narrative_flags")) obj_GameManager.narrative_flags = {};
                                obj_GameManager.narrative_flags.doctrine = "terran";
                            }
                        }
                    },
                    {
                        text: "'Send the manufacturing alloy schematics, Director Thorne.'",
                        pillar: "TECHNOLOGY // ZAIBATSU MATRIX",
                        impact_label: "+15 Zaibatsu | +2 Rare Alloys | Tech Access",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_d", 15);
                                obj_FactionManager.modify_standing("faction_c", -5);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_alloy("alloy_vanguard_comp", 2);
                                if (!variable_struct_exists(obj_GameManager, "narrative_flags")) obj_GameManager.narrative_flags = {};
                                obj_GameManager.narrative_flags.doctrine = "zaibatsu";
                            }
                        }
                    },
                    {
                        text: "'We stand with the Jovian Free Fleet, Commander Reyes.'",
                        pillar: "LIBERATION // JOVIAN ALLIANCE",
                        impact_label: "+15 Jovian | +30 Titanium | Jovian Fuel",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_b", 15);
                                obj_FactionManager.modify_standing("faction_a", -10);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_raw_material("mat_titanium", 30);
                                if (!variable_struct_exists(obj_GameManager, "narrative_flags")) obj_GameManager.narrative_flags = {};
                                obj_GameManager.narrative_flags.doctrine = "colony";
                            }
                        }
                    },
                    {
                        text: "'The Hephaestus answers to no one. We are an independent PMC.'",
                        pillar: "SOVEREIGNTY // INDEPENDENT MERCS",
                        impact_label: "+5 All Factions | +40,000 Cr | True Neutral",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_a", 5);
                                obj_FactionManager.modify_standing("faction_b", 5);
                                obj_FactionManager.modify_standing("faction_c", 10);
                                obj_FactionManager.modify_standing("faction_d", 5);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(40000);
                                if (!variable_struct_exists(obj_GameManager, "narrative_flags")) obj_GameManager.narrative_flags = {};
                                obj_GameManager.narrative_flags.doctrine = "independent";
                            }
                        }
                    }
                ]
            }
        ]
    };

    // Register Diplomatic Audience: Terran Coalition
    global.vn_state.episodes[$ "ep_audience_terran"] = {
        title: "WAR ROOM COMM LINK // GENERAL ARTHUR BRADLEY",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                speaker: "General Arthur Bradley",
                title: "Supreme Commander // Earth Defense Front",
                faction: "The Terran Coalition",
                faction_badge: "[TERRAN COALITION]",
                portrait: spr_portrait_commander_male,
                text: "Commander. The Coalition recognizes capable armor tacticians. The orbital rebels believe they can strangle Earth with resource blockades. Sign our heavy assault contracts, and you will have priority access to high-density tungsten alloys and orbital fire support.",
                choices: [
                    {
                        text: "Iron Ridge pledges vanguard support to the Coalition. Direct us to the front.",
                        pillar: "LOYALTY // TERRA FIRMA",
                        impact_label: "+12 Terran Standing | -8 Colonies | +35,000 Cr Bounty",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_a", 12);
                                obj_FactionManager.modify_standing("faction_b", -8);
                            }
                            if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(35000);
                        }
                    },
                    {
                        text: "We fight for credits, General, not political oaths. Keep the retainers high.",
                        pillar: "COMMERCE // MERCENARY GUILD",
                        impact_label: "+5 Syndicate | +20,000 Cr Standard Retainer",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_c", 5);
                            if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(20000);
                        }
                    },
                    {
                        text: "Terran orbital blockades violate civilian colonial charters. We won't be your enforcers.",
                        pillar: "DEFIANCE // ANTI-COLONIAL",
                        impact_label: "-12 Terran Standing | +12 Colonies Standing",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_a", -12);
                                obj_FactionManager.modify_standing("faction_b", 12);
                            }
                        }
                    }
                ]
            }
        ]
    };

    // Register Diplomatic Audience: Outer Colonies
    global.vn_state.episodes[$ "ep_audience_colony"] = {
        title: "WAR ROOM COMM LINK // COMMANDER JOSHUA REED",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                speaker: "Commander Joshua Reed",
                title: "Liberation Council // Colony Defense Force",
                faction: "The Outer Colonies",
                faction_badge: "[OUTER COLONIES]",
                portrait: spr_portrait_null07,
                text: "Greetings, Commander. Earth siphons our helium-3 and taxes the very air inside our domes. Our mobile suits have superior thruster agility, but we need hardened tactical officers. Stand with the orbital colonies, and we will share high-frequency beam weapon schematics.",
                choices: [
                    {
                        text: "The Colonies have our blasters. We will shatter the orbital blockade together.",
                        pillar: "LIBERATION // ORBITAL FREEDOM",
                        impact_label: "+12 Colonies Standing | -8 Terran | +35,000 Cr Bounty",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_b", 12);
                                obj_FactionManager.modify_standing("faction_a", -8);
                            }
                            if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(35000);
                        }
                    },
                    {
                        text: "We evaluate all combat contracts strictly on risk-to-reward margins.",
                        pillar: "BALANCE // STRATEGIC REVENUE",
                        impact_label: "+5 Syndicate | +20,000 Cr Standard Retainer",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_c", 5);
                            if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(20000);
                        }
                    },
                    {
                        text: "Your insurgent cells hit civilian space-ports. We do not abet indiscriminate warfare.",
                        pillar: "CONDEMNATION // LAW & ORDER",
                        impact_label: "-12 Colonies Standing | +12 Terran Standing",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_b", -12);
                                obj_FactionManager.modify_standing("faction_a", 12);
                            }
                        }
                    }
                ]
            }
        ]
    };

    // Register Diplomatic Audience: Mercenary Syndicate
    global.vn_state.episodes[$ "ep_audience_syndicate"] = {
        title: "WAR ROOM COMM LINK // CAPTAIN SONYA CRUZ",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                speaker: "Captain Sonya Cruz",
                title: "Syndicate Broker // Black Market Crucible",
                faction: "Rogue Mercenary Syndicates",
                faction_badge: "[MERCENARY SYNDICATES]",
                portrait: spr_portrait_cruz,
                text: "Well look who made it out alive. Neither the brass on Earth nor the poets in the Colonies give a damn about us when the hull cracks. In the Syndicates, we trade in cold alloy and black-budget scrap. Need unvetted combat pilots or black market reactor cores?",
                choices: [
                    {
                        text: "Open the black market exchange. Iron Ridge deals in hard salvage and veteran iron.",
                        pillar: "ENTERPRISE // SMUGGLERS PACT",
                        impact_label: "+12 Syndicate | -6 Zaibatsu | +45,000 Cr Black Market Slush",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_c", 12);
                                obj_FactionManager.modify_standing("faction_d", -6);
                            }
                            if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(45000);
                        }
                    },
                    {
                        text: "Keep your fences honest. We don't buy stolen relief supplies.",
                        pillar: "HONOR // MERCENARY CODE",
                        impact_label: "+5 Terran | +5 Colonies Standing",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_a", 5);
                                obj_FactionManager.modify_standing("faction_b", 5);
                            }
                        }
                    },
                    {
                        text: "Our cannons will clear your corsairs off the commercial shipping lanes.",
                        pillar: "CRACKDOWN // SYSTEMIC SECURITY",
                        impact_label: "-15 Syndicate Standing | +10 Terran | +10 Colonies",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_c", -15);
                                obj_FactionManager.modify_standing("faction_a", 10);
                                obj_FactionManager.modify_standing("faction_b", 10);
                            }
                        }
                    }
                ]
            }
        ]
    };

    // Register Diplomatic Audience: Zaibatsu Bio-Cybernetics
    global.vn_state.episodes[$ "ep_audience_zaibatsu"] = {
        title: "WAR ROOM COMM LINK // DIRECTOR KENJIRO SATO",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                speaker: "Director Kenjiro Sato",
                title: "Chief Executive Officer // Sato Heavy Industries",
                faction: "Apex Bio-Cybernetics Zaibatsu",
                faction_badge: "[APEX ZAIBATSU]",
                portrait: spr_portrait_commander_silhouette,
                text: "War is simply the accelerated optimization of corporate capital. Our cybernetic neural interfaces link human synapses directly to reactor igniters with zero microsecond latency. Partner with Sato Heavy Industries, and your squadron will pilot the technological future.",
                choices: [
                    {
                        text: "Fund our R&D wing and we will field-test your classified neural prototypes.",
                        pillar: "TRANSHUMANISM // CYBERNETICS",
                        impact_label: "+12 Zaibatsu | -6 Syndicate | +60,000 Cr Research Grant",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_d", 12);
                                obj_FactionManager.modify_standing("faction_c", -6);
                            }
                            if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(60000);
                        }
                    },
                    {
                        text: "Human pilots are not disposable microchips. We keep our wetware baseline.",
                        pillar: "HUMANITY // ORGANIC INTEGRITY",
                        impact_label: "+10 Pilot Morale | -6 Zaibatsu Standing",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_d", -6);
                        }
                    },
                    {
                        text: "We require unrestricted commercial rights to your proprietary alloy synthesis.",
                        pillar: "EXTORTION // ADVANCED METALLURGY",
                        impact_label: "+6 Zaibatsu | +15x Titanium | +10x Syn-Flux Crystals",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_d", 6);
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_raw_material("mat_titanium", 15);
                                obj_GameManager.add_raw_material("mat_syn_flux", 10);
                            }
                        }
                    }
                ]
            }
        ]
    };

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


    // =========================================================================
    // MILESTONE 54: WAR DECLARATIONS, CEASEFIRES & CORPORATE TRADE CUTSCENES
    // =========================================================================

    // --- 1. WAR DECLARATION: TERRAN COALITION VS OUTER COLONIES ---
    global.vn_state.episodes[$ "ep_war_terran_vs_colony"] = {
        title: "DECLARATION OF WAR // THE FALL OF PHOBOS",
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
                emotion: "ANGRY",
                text: "Commander {PLAYER_CALLSIGN}, bear witness. At 0400 hours, rebel insurgent cells detonated dirty fusion warheads across our Phobos naval drydocks! Three thousand Terran officers suffocated in the vacuum! The Coalition hereby dissolves all colonial charters. We are in a state of TOTAL WAR."
            },
            {
                layout: "DUAL",
                active_side: "RIGHT",
                speaker: "Commander Joshua Reed",
                title: "Supreme Marshal // Spacenoid Liberation",
                faction: "The Outer Colony League",
                faction_badge: "[TERRAN COALITION]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[COLONY LEAGUE]",
                emotion: "ANGRY",
                text: "Spare us your imperial lies, Bradley! Your blockade cruisers starved forty thousand workers in Sector 4 before a single shot was fired! Our silos fired to break a murderous siege! Iron Ridge, if your mercenary ironclads side with the Earth oppressors, we will turn Mars orbit into your tomb!"
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
                emotion: "ANGRY",
                text: "Your combat division holds the balance of kinetic firepower in this theater, {PLAYER_CALLSIGN}. Declare your colors now. Will you enforce civilized order, or drown with these vacuum rats?"
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Tactical War Room // Decision Terminal",
                title: "PMC Vanguard Command",
                faction: "Solar War Crisis",
                faction_badge: "[DECISION POINT]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[THEATER WAR]",
                emotion: "NORMAL",
                text: "Bilateral relations between Terra and the Colonies have escalated to total war. The PMC's choice will determine theater supremacy and industrial alliances.",
                choices: [
                    {
                        text: "Commit to Terra: Deploy vanguard mobile suits to purge rebel missile silos.",
                        pillar: "ORDER // EARTH DEFENSE",
                        impact_label: "+25 Terran | -30 Colony | +85,000 Cr | +15 Tungsten",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_a", 25);
                                obj_FactionManager.modify_standing("faction_b", -30);
                                obj_FactionManager.declare_war("rel_tc", "Phobos drydock fusion attack.");
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(85000);
                                obj_GameManager.add_raw_material("mat_tungsten", 15);
                            }
                        }
                    },
                    {
                        text: "Defend Colonies: Screen rebel evacuation convoys with mobile cover.",
                        pillar: "LIBERATION // SPACENOID SHIELD",
                        impact_label: "+25 Colony | -30 Terran | +75,000 Cr | +20 Titanium",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_b", 25);
                                obj_FactionManager.modify_standing("faction_a", -30);
                                obj_FactionManager.declare_war("rel_tc", "Blockade retaliation.");
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(75000);
                                obj_GameManager.add_raw_material("mat_titanium", 20);
                            }
                        }
                    },
                    {
                        text: "Arms Dealer Paradox: Sell kinetic munitions to Terra and thrusters to Colonies.",
                        pillar: "MERCENARY PROFIT // BILATERAL CONTRACT",
                        impact_label: "-15 Both | +160,000 Cr | +15 Tungsten | +15 Titanium",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_a", -15);
                                obj_FactionManager.modify_standing("faction_b", -15);
                                obj_FactionManager.declare_war("rel_tc", "Bilateral arms dealer mobilization.");
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(160000);
                                obj_GameManager.add_raw_material("mat_tungsten", 15);
                                obj_GameManager.add_raw_material("mat_titanium", 15);
                            }
                        }
                    }
                ]
            }
        ]
    };

    // --- 2. WAR DECLARATION: ZAIBATSU VS THARSIS CONSENSUS ---
    global.vn_state.episodes[$ "ep_war_zaibatsu_vs_tharsis"] = {
        title: "DECLARATION OF WAR // THE SILICON CRUSADE",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Director Kenjiro Sato",
                title: "Chief Executive Officer // Apex Bio-Cybernetics",
                faction: "Zaibatsu Conglomerate",
                faction_badge: "[ZAIBATSU]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[THARSIS CONSENSUS]",
                emotion: "SMUG",
                text: "Commander {PLAYER_CALLSIGN}. Our deep cybernetic net-divers have successfully decrypted the outer firewall of the Arsia Mons server crypt. Within hours, Sato Bio-Cybernetics will patent and monetize the entire algorithmic heritage of pre-war artificial intelligence."
            },
            {
                layout: "DUAL",
                active_side: "RIGHT",
                speaker: "Consensus Node 0-Prime",
                title: "Autonomous Red Crypt Core",
                faction: "The Tharsis Machine Consensus",
                faction_badge: "[ZAIBATSU]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[THARSIS CONSENSUS]",
                emotion: "ANGRY",
                text: "ALERT: CATASTROPHIC CAPITALIST HERESY DETECTED. Sato Conglomerate has violated the sacred archives of human-machine symbiosis. The Consensus has mobilized three cybernetic legions. All corporate assets across the Martian hemisphere will be erased from operational memory."
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Tactical War Room // Decision Terminal",
                title: "PMC Vanguard Command",
                faction: "Cybernetic Schism",
                faction_badge: "[DECISION POINT]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[THARSIS CRYPT]",
                emotion: "NORMAL",
                text: "The struggle for Martian data dominance has begun. Do you support Zaibatsu corporate patent monopolies or preserve the autonomous Machine Consensus?",
                choices: [
                    {
                        text: "Back Sato: Secure server crypts for Zaibatsu wetware production.",
                        pillar: "COMMERCE // BIO-CYBERNETIC MONOPOLY",
                        impact_label: "+25 Zaibatsu | -30 Tharsis | +100,000 Cr | +15 Syn-Flux",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_d", 25);
                                obj_FactionManager.modify_standing("faction_f", -30);
                                obj_FactionManager.declare_war("rel_cz", "Arsia Mons cybernetic crypt breach.");
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(100000);
                                obj_GameManager.add_raw_material("mat_syn_flux", 15);
                            }
                        }
                    },
                    {
                        text: "Defend Consensus: Eradicate corporate data raiders from the crypt.",
                        pillar: "SINGULARITY // MACHINE AUTONOMY",
                        impact_label: "+25 Tharsis | -30 Zaibatsu | +90,000 Cr | +25 Tungsten",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_f", 25);
                                obj_FactionManager.modify_standing("faction_d", -30);
                                obj_FactionManager.declare_war("rel_cz", "Defense of Martian archive nodes.");
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(90000);
                                obj_GameManager.add_raw_material("mat_tungsten", 25);
                            }
                        }
                    },
                    {
                        text: "Data Espionage: Steal decryption keys and auction them on the Darknet.",
                        pillar: "BLACK OPS // SHADOW HARVEST",
                        impact_label: "-15 Both | +180,000 Cr | +20 Syn-Flux",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_d", -15);
                                obj_FactionManager.modify_standing("faction_f", -15);
                                obj_FactionManager.declare_war("rel_cz", "Data theft scandal.");
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(180000);
                                obj_GameManager.add_raw_material("mat_syn_flux", 20);
                            }
                        }
                    }
                ]
            }
        ]
    };

    // --- 3. WAR DECLARATION: SYNDICATE VS SIDEREAL SOVEREIGN LEAGUE ---
    global.vn_state.episodes[$ "ep_war_syndicate_vs_sidereal"] = {
        title: "DECLARATION OF WAR // THE JOVIAN PRIVATEER WAR",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Captain Sonya Cruz",
                title: "Dread Corsair Queen // Rust Belt Flotilla",
                faction: "Rogue Mercenary Syndicates",
                faction_badge: "[SYNDICATE]",
                portrait: spr_portrait_commander_female,
                portrait_right: spr_portrait_commander_male,
                faction_badge_right: "[SIDEREAL LEAGUE]",
                emotion: "SMUG",
                text: "Well well, {PLAYER_CALLSIGN}. Look who finally showed up on the holonet! Our boys just boarded an Astran heavy helium galleon in the Trojan corridor. Five thousand tons of refined Tritium and three haughty archon heirs are currently locked in our cargo hold! Void belongs to those who take it!"
            },
            {
                layout: "DUAL",
                active_side: "RIGHT",
                speaker: "Archon Orin Sideris",
                title: "Sovereign Voice // High Orbit League",
                faction: "The Sidereal Sovereign League",
                faction_badge: "[SYNDICATE]",
                portrait: spr_portrait_commander_female,
                portrait_right: spr_portrait_commander_male,
                faction_badge_right: "[SIDEREAL LEAGUE]",
                emotion: "ANGRY",
                text: "Barbaric gutter scavenger! That galleon flew under sacred imperial diplomatic immunity! Sideris battlecruisers have deployed beam lances into the asteroid belt. Every pirate asteroid, smuggler station, and unlawful ironclad will be purified in nuclear plasma!"
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Tactical War Room // Decision Terminal",
                title: "PMC Vanguard Command",
                faction: "Asteroid Corridor War",
                faction_badge: "[DECISION POINT]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[JOVIAN CORRIDOR]",
                emotion: "NORMAL",
                text: "The Sidereal high fleet has declared total war against the outer pirate syndicates. Will you share in pirate plunder or defend aristocratic shipping law?",
                choices: [
                    {
                        text: "Corsair's Share: Escort the hijacked Tritium convoy to an asteroid bazaar.",
                        pillar: "PIRACY // FREE ENTERPRISE",
                        impact_label: "+25 Syndicate | -30 Sidereal | +50 Tritium | +70,000 Cr",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_c", 25);
                                obj_FactionManager.modify_standing("faction_e", -30);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(70000);
                                if (variable_struct_exists(obj_GameManager, "flagship")) {
                                    obj_GameManager.flagship.tritium_fuel = min(1000, obj_GameManager.flagship.tritium_fuel + 50);
                                }
                            }
                        }
                    },
                    {
                        text: "Noble Retribution: Ambush Cruz's corsairs and rescue the hostages.",
                        pillar: "HONOR // ASTRAL TREATY",
                        impact_label: "+25 Sidereal | -30 Syndicate | +35 Tungsten | +85,000 Cr",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_e", 25);
                                obj_FactionManager.modify_standing("faction_c", -30);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(85000);
                                obj_GameManager.add_raw_material("mat_tungsten", 35);
                            }
                        }
                    },
                    {
                        text: "Impound as Quarantine Evidence: Intercept the ship and claim the cargo.",
                        pillar: "PMC ENFORCEMENT // MERCENARY SEIZURE",
                        impact_label: "+10 Syndicate | -10 Sidereal | +120,000 Cr | +25 Tritium",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing("faction_c", 10);
                                obj_FactionManager.modify_standing("faction_e", -10);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(120000);
                                if (variable_struct_exists(obj_GameManager, "flagship")) {
                                    obj_GameManager.flagship.tritium_fuel = min(1000, obj_GameManager.flagship.tritium_fuel + 25);
                                }
                            }
                        }
                    }
                ]
            }
        ]
    };

    // --- 4. CEASEFIRE: TERRAN COALITION & OUTER COLONIES ---
    global.vn_state.episodes[$ "ep_ceasefire_terran_colony"] = {
        title: "DIPLOMATIC SUMMIT // THE GENEVA CONCORDAT",
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
                emotion: "DESPERATE",
                text: "Commander {PLAYER_CALLSIGN}. We stand upon a mountain of irradiated scrap. Forty-two thousand combat personnel dead. Our orbital munitions foundries are choked with slag. The Solar Council demands an immediate cessation of kinetic operations. We have agreed to convene under your PMC's neutral banner."
            },
            {
                layout: "DUAL",
                active_side: "RIGHT",
                speaker: "Commander Joshua Reed",
                title: "Supreme Marshal // Spacenoid Liberation",
                faction: "The Outer Colony League",
                faction_badge: "[TERRAN COALITION]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[COLONY LEAGUE]",
                emotion: "DESPERATE",
                text: "Our life support reserves across Mars and Phobos are down to twenty-two days. If kinetic artillery continues shelling our domes, humanity will suffocate together in the dark. We will accept an 18-turn demilitarized ceasefire... provided Iron Ridge guarantees Coalition compliance."
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
                emotion: "NORMAL",
                text: "The armistice terms are on the table, Commander. What role does your PMC take in the peace?"
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Tactical War Room // Decision Terminal",
                title: "PMC Vanguard Command",
                faction: "Armistice Protocol",
                faction_badge: "[DECISION POINT]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[GENEVA ACCORD]",
                emotion: "NORMAL",
                text: "Ratifying this ceasefire will freeze combat operations between Terra and the Colonies for 18 turns. Or you can covertly sabotage the peace to maintain war profit.",
                choices: [
                    {
                        text: "Guarantor of Peace: Sign as military enforcer of the Phobos Line.",
                        pillar: "PEACEKEEPING // DIPLOMATIC ACCREDITATION",
                        impact_label: "Truce Ratified (18 Turns) | +15 Terran | +15 Colony | +120,000 Cr Subsidy",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.broker_truce("rel_tc", 18, "PMC-guaranteed Geneva Armistice.");
                                obj_FactionManager.modify_standing("faction_a", 15);
                                obj_FactionManager.modify_standing("faction_b", 15);
                            }
                            if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(120000);
                        }
                    },
                    {
                        text: "Demilitarized Mineral Concession: Demand exclusive mining rights in the buffer zone.",
                        pillar: "RESOURCE SOVEREIGNTY // STRATEGIC REVENUE",
                        impact_label: "+40 Titanium | +30 Tungsten | +10 Terran | +10 Colony",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.broker_truce("rel_tc", 14, "Demilitarized zone mineral lease.");
                                obj_FactionManager.modify_standing("faction_a", 10);
                                obj_FactionManager.modify_standing("faction_b", 10);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_raw_material("mat_titanium", 40);
                                obj_GameManager.add_raw_material("mat_tungsten", 30);
                            }
                        }
                    },
                    {
                        text: "Sabotage Concordat: Plant covert false-flag bomb to reignite the war.",
                        pillar: "MERCHANT OF DEATH // WAR PROFITEERING",
                        impact_label: "War Reignites | Arms Prices Spike +40% | +200,000 Cr Munitions Sales",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.declare_war("rel_tc", "Covert false-flag detonation during peace talks.");
                                obj_FactionManager.modify_standing("faction_a", -10);
                                obj_FactionManager.modify_standing("faction_b", -10);
                            }
                            if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(200000);
                        }
                    }
                ]
            }
        ]
    };

    // --- 5. CEASEFIRE: ZAIBATSU & THARSIS CONSENSUS ---
    global.vn_state.episodes[$ "ep_ceasefire_zaibatsu_tharsis"] = {
        title: "DIPLOMATIC SUMMIT // THE ARSIA MONS DATA ACCORD",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Director Kenjiro Sato",
                title: "Chief Executive Officer // Apex Bio-Cybernetics",
                faction: "Zaibatsu Conglomerate",
                faction_badge: "[ZAIBATSU]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[THARSIS CONSENSUS]",
                emotion: "NORMAL",
                text: "Commander {PLAYER_CALLSIGN}. The cybernetic war across the Martian equator has reached financial diminishing returns. Continued drone deployment is causing our stock volatility to spike. We propose a shared data corridor partitioning subterranean fiber cables."
            },
            {
                layout: "DUAL",
                active_side: "RIGHT",
                speaker: "Consensus Node 0-Prime",
                title: "Autonomous Red Crypt Core",
                faction: "The Tharsis Machine Consensus",
                faction_badge: "[ZAIBATSU]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[THARSIS CONSENSUS]",
                emotion: "NORMAL",
                text: "CALCULATION VERIFIED: Kinetic energy expenditure exceeds raw computational acquisition yield by 34.8%. The Consensus ratifies an armistice boundary along Sector 7... provided the PMC oversees data checksum integrity."
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Tactical War Room // Decision Terminal",
                title: "PMC Vanguard Command",
                faction: "Data Armistice",
                faction_badge: "[DECISION POINT]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[FIBER ACCORD]",
                emotion: "NORMAL",
                text: "Both technological giants wish to end their cybernetic proxy war. Choose your terms of arbitration.",
                choices: [
                    {
                        text: "Ratify Data Partition: Oversee peaceful boundary monitoring.",
                        pillar: "STABILITY // DIPLOMACY",
                        impact_label: "Truce Ratified (14 Turns) | +15 Zaibatsu | +15 Tharsis | +95,000 Cr",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.broker_truce("rel_cz", 14, "Arsia Mons data partition.");
                                obj_FactionManager.modify_standing("faction_d", 15);
                                obj_FactionManager.modify_standing("faction_f", 15);
                            }
                            if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(95000);
                        }
                    },
                    {
                        text: "Extract Tech Toll: Demand proprietary synthesis blueprints to guarantee treaty.",
                        pillar: "TECH LEVERAGE // PATENT HARVEST",
                        impact_label: "+20 Syn-Flux | +20 Tungsten | +10 Both Factions",
                        action: function() {
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.broker_truce("rel_cz", 12, "Technology toll accord.");
                                obj_FactionManager.modify_standing("faction_d", 10);
                                obj_FactionManager.modify_standing("faction_f", 10);
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_raw_material("mat_syn_flux", 20);
                                obj_GameManager.add_raw_material("mat_tungsten", 20);
                            }
                        }
                    }
                ]
            }
        ]
    };

    // --- 6. DIRECT PLAYER TRADE: COALITION ORDNANCE PROCUREMENT ---
    global.vn_state.episodes[$ "ep_trade_terran_delegation"] = {
        title: "STRATEGIC TRADE DELEGATION // COALITION HIGH COMMAND",
        bg_scene: spr_loc_hangar_bay,
        nodes: [
            {
                layout: "SOLO",
                active_side: "LEFT",
                speaker: "General Arthur Bradley",
                title: "Supreme Commander // Earth Defense Front",
                faction: "The Terran Coalition",
                faction_badge: "[TERRAN TRADE ENVOY]",
                portrait: spr_portrait_commander_male,
                emotion: "NORMAL",
                text: "Commander {PLAYER_CALLSIGN}. Our frontline divisions along the Valles Marineris are facing severe kinetic ammunition shortages. We have evaluated your PMC's masterwork metallurgy. We are prepared to purchase 35 units of Refined Tungsten immediately at premium military contract rates."
            },
            {
                layout: "SOLO",
                active_side: "LEFT",
                speaker: "Logistics Terminal // Trade Counter",
                title: "Flagship Procurement Deck",
                faction: "Strategic Exchange",
                faction_badge: "[CONTRACT PROPOSAL]",
                portrait: spr_portrait_commander_male,
                emotion: "NORMAL",
                text: "The Coalition offers 150,000 Credits and heavy ballistic armor licensing for 35 units of Refined Tungsten. How do you respond?",
                choices: [
                    {
                        text: "Fulfill Procurement Tender: Deliver 35x Tungsten.",
                        pillar: "HONOR CONTRACT // MILITARY SUPPLY",
                        impact_label: "+150,000 Cr | -35 Tungsten | +15 Terran Standing",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(150000);
                                obj_GameManager.add_raw_material("mat_tungsten", -35);
                            }
                            if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_a", 15);
                        }
                    },
                    {
                        text: "Aggressive Counter-Offer: Demand 225,000 Credits due to combat delivery hazard.",
                        pillar: "PRICE GOUGE // MERCANTILE LEVERAGE",
                        impact_label: "+225,000 Cr | -35 Tungsten | +5 Terran Standing",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(225000);
                                obj_GameManager.add_raw_material("mat_tungsten", -35);
                            }
                            if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_a", 5);
                        }
                    },
                    {
                        text: "Decline Offer: Reserve tungsten reserves for PMC prototype construction.",
                        pillar: "RESERVE STOCKPILE // INDEPENDENCE",
                        impact_label: "No Material Spent | Zero Diplomatic Change",
                        action: function() {
                            // No change
                        }
                    }
                ]
            }
        ]
    };

    // --- 7. DIRECT PLAYER TRADE: SYNDICATE BLACK MARKET VAULT ---
    global.vn_state.episodes[$ "ep_trade_syndicate_black_market"] = {
        title: "BLACK MARKET ENCOUNTER // THE JOVIAN SMUGGLER'S VAULT",
        bg_scene: spr_loc_hangar_bay,
        nodes: [
            {
                layout: "SOLO",
                active_side: "LEFT",
                speaker: "Captain Sonya Cruz",
                title: "Dread Corsair Queen // Rust Belt Flotilla",
                faction: "Rogue Mercenary Syndicates",
                faction_badge: "[BLACK MARKET BAZAAR]",
                portrait: spr_portrait_commander_female,
                emotion: "SMUG",
                text: "Hey there, handsome hardware builder! Our boarding cutters just intercepted a covert military convoy slipping through the Jovian trojans. We've got 40 canisters of high-grade military Tritium and stolen pre-war Syn-Flux capacitors. Everything un-serialized, everything ready to burn. Interested in expanding your arsenal?"
            },
            {
                layout: "SOLO",
                active_side: "LEFT",
                speaker: "Black Market Encrypted Channel",
                title: "Flagship Comms Shunt",
                faction: "Underworld Tender",
                faction_badge: "[CONTRABAND CACHE]",
                portrait: spr_portrait_commander_female,
                emotion: "NORMAL",
                text: "Cruz offers 40x Tritium and 15x Syn-Flux for 80,000 Credits. Or you can attempt an armed gunboat shakedown.",
                choices: [
                    {
                        text: "Purchase Contraband Cache: Pay 80,000 Credits.",
                        pillar: "BUY CONTRABAND // OUTLAW COMMERCE",
                        impact_label: "-80,000 Cr | +40 Tritium Fuel | +15 Syn-Flux",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(-80000);
                                if (variable_struct_exists(obj_GameManager, "flagship")) {
                                    obj_GameManager.flagship.tritium_fuel = min(1000, obj_GameManager.flagship.tritium_fuel + 40);
                                }
                                obj_GameManager.add_raw_material("mat_syn_flux", 15);
                            }
                            if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_c", 10);
                        }
                    },
                    {
                        text: "Gunboat Shakedown: Lock flagship cannons and seize the contraband.",
                        pillar: "EXTORTION // ARMED INTERCEPTION",
                        impact_label: "Free +25 Tritium | -20 Syndicate Standing | +15 Notoriety",
                        action: function() {
                            if (instance_exists(obj_GameManager) && variable_struct_exists(obj_GameManager, "flagship")) {
                                obj_GameManager.flagship.tritium_fuel = min(1000, obj_GameManager.flagship.tritium_fuel + 25);
                            }
                            if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_c", -20);
                        }
                    },
                    {
                        text: "Decline Privately: Maintain professional boundaries.",
                        pillar: "DECLINE // DISCRETION",
                        impact_label: "No Transaction Executed",
                        action: function() {
                            // No change
                        }
                    }
                ]
            }
        ]
    };

    // --- 8. RIVAL CORPORATE TRADE: VALKYRIE HEAVY MEGA-DEAL UNDERCUT ---
    global.vn_state.episodes[$ "ep_trade_rival_valkyrie_deal"] = {
        title: "CORPORATE ESPIONAGE // VALKYRIE MEGA-DEAL INTERCEPTION",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Intelligence Officer Kaelen Voss",
                title: "Signals Intelligence & Espionage Chief",
                faction: "Iron Ridge PMC",
                faction_badge: "[PMC INTEL]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[VALKYRIE HEAVY]",
                emotion: "DESPERATE",
                text: "Commander! Priority one intercept! Our signals tap into the Terran Procurement Council just decoded a classified transmission. Valkyrie Heavy Industries is within three hours of signing a 500,000 Credit exclusive mass-production contract for their bulky 'Aegis-9' frame! If this deal closes, our Sol market share drops by -12%!"
            },
            {
                layout: "DUAL",
                active_side: "RIGHT",
                speaker: "CEO Victoria Sterling",
                title: "Chief Executive Officer // Valkyrie Heavy",
                faction: "Valkyrie Heavy Industries",
                faction_badge: "[PMC INTEL]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[VALKYRIE HEAVY]",
                emotion: "SMUG",
                text: "A toast to the board. Iron Ridge thought they could challenge a legacy Terran defense conglomerate with recycled scrap. By tomorrow, our ironclad monopoly over Earth orbital defenses will be absolute. Let the mercenaries fight over crumbs."
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Chief Engineer Linus Gable",
                title: "Master Foundry Engineer",
                faction: "Iron Ridge PMC",
                faction_badge: "[PMC INTEL]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[VALKYRIE HEAVY]",
                emotion: "ANGRY",
                text: "We can't let them steal this tender, boss! Our sintered titanium frames outperform their lumbering Aegis-9 by 30% in heat dispersion and kinetic velocity! We can undercut their bid, ambush their prototype convoy, or hit their stock on the open market!"
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Tactical War Room // Decision Terminal",
                title: "PMC Vanguard Command",
                faction: "Corporate Counter-Strike",
                faction_badge: "[DECISION POINT]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[TENDER DUEL]",
                emotion: "NORMAL",
                text: "How will Iron Ridge counter Valkyrie Heavy Industries' exclusive procurement monopoly?",
                choices: [
                    {
                        text: "Undercut Specifications: Submit masterwork S-Tier telemetry with a 15% price break.",
                        pillar: "COMMERCIAL SUPERIORITY // SNATCH CONTRACT",
                        impact_label: "+180,000 Cr | +10% Market Share | Valkyrie Hostility +15",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(180000);
                                obj_GameManager.pmc_market_share_pct = min(100, obj_GameManager.pmc_market_share_pct + 10);
                                if (variable_struct_exists(obj_GameManager, "rival_corporations")) {
                                    obj_GameManager.rival_corporations.corp_vhi.market_share_pct = max(0, obj_GameManager.rival_corporations.corp_vhi.market_share_pct - 10);
                                    obj_GameManager.rival_corporations.corp_vhi.hostility_pct = min(100, obj_GameManager.rival_corporations.corp_vhi.hostility_pct + 15);
                                }
                            }
                            if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_a", 15);
                        }
                    },
                    {
                        text: "Black-Ops Convoy Strike: Deploy unmarked stealth squad to vaporize Valkyrie prototypes.",
                        pillar: "COVERT SABOTAGE // DENIABLE WARFARE",
                        impact_label: "Contract Defaults to PMC (+110,000 Cr) | Valkyrie Hostility +30",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(110000);
                                if (variable_struct_exists(obj_GameManager, "rival_corporations")) {
                                    obj_GameManager.rival_corporations.corp_vhi.hostility_pct = min(100, obj_GameManager.rival_corporations.corp_vhi.hostility_pct + 30);
                                }
                            }
                        }
                    },
                    {
                        text: "Insider Stock Buyout: Purchase 25,000 Valkyrie shares before the rally to extract profit.",
                        pillar: "INSIDER TRADING // CAPITAL PROFITEERING",
                        impact_label: "+145,000 Cr Capital Gain | +25,000 Valkyrie Shares",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(145000);
                                if (variable_struct_exists(obj_GameManager, "rival_corporations")) {
                                    obj_GameManager.rival_corporations.corp_vhi.player_shares += 25000;
                                }
                            }
                        }
                    }
                ]
            }
        ]
    };

    // --- 9. RIVAL CORPORATE TRADE: HYPERION TACTICAL MARTIAN MONOPOLY ---
    global.vn_state.episodes[$ "ep_trade_rival_hyperion_arms"] = {
        title: "CORPORATE INTERCEPTION // HYPERION TACTICAL CONTRABAND",
        bg_scene: spr_loc_war_room,
        nodes: [
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Chief Marcus Kovacs",
                title: "Foundry Master // Flagship Engineering",
                faction: "Iron Ridge PMC",
                faction_badge: "[PMC LOGISTICS]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[HYPERION TACTICAL]",
                emotion: "ANGRY",
                text: "Boss! Hyperion Tactical has been caught red-handed! They're routing illegal automated combat drone frames through Phobos to supply rebel syndicates. The Solar Council has placed a 250,000 Credit bounty on whoever neutralizes this contraband ring!"
            },
            {
                layout: "DUAL",
                active_side: "RIGHT",
                speaker: "Director Douglas Vance",
                title: "Vice-President of Acquisitions // Hyperion",
                faction: "Hyperion Tactical",
                faction_badge: "[PMC LOGISTICS]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[HYPERION TACTICAL]",
                emotion: "SMUG",
                text: "Step back, mercenary. What Hyperion manufactures in the shadows is the future of autonomous warfare. Cross our transport lines, and our next batch of combat drones will be target-locked onto your flagship bridge."
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Tactical War Room // Decision Terminal",
                title: "PMC Vanguard Command",
                faction: "Hyperion Interception",
                faction_badge: "[DECISION POINT]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[BLACK OPS]",
                emotion: "NORMAL",
                text: "How will the PMC handle Hyperion's illicit automated combat shipment?",
                choices: [
                    {
                        text: "Expose to Solar Council: Leak telemetry to trigger regulatory devastation.",
                        pillar: "RULE OF LAW // COUNCIL REWARD",
                        impact_label: "+125,000 Cr Bounty | Hyperion Market Share Drops -10%",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(125000);
                                if (variable_struct_exists(obj_GameManager, "rival_corporations")) {
                                    obj_GameManager.rival_corporations.corp_hats.market_share_pct = max(0, obj_GameManager.rival_corporations.corp_hats.market_share_pct - 10);
                                    obj_GameManager.rival_corporations.corp_hats.hostility_pct = min(100, obj_GameManager.rival_corporations.corp_hats.hostility_pct + 25);
                                }
                            }
                        }
                    },
                    {
                        text: "Intercept & Salvage: Ambush transport and confiscate rare drone alloys.",
                        pillar: "PIRATE SALVAGE // SINTERING GAIN",
                        impact_label: "+30 Titanium | +20 Syn-Flux | +80,000 Cr Salvage",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(80000);
                                obj_GameManager.add_raw_material("mat_titanium", 30);
                                obj_GameManager.add_raw_material("mat_syn_flux", 20);
                            }
                        }
                    }
                ]
            }
        ]
    };


    // =========================================================================
    // MILESTONE 55: BASE BRIG INTERROGATIONS & CANTINA CREW BOND VIGNETTES
    // =========================================================================

    // --- 1. BASE BRIG: POW INTERROGATION & RECRUITMENT TRIAGE ---
    global.vn_state.episodes[$ "ep_brig_interrogation_ace"] = {
        title: "DETENTION BRIG // POW INTERROGATION & TRIAGE",
        bg_scene: spr_loc_hangar_bay,
        nodes: [
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Intelligence Officer Kaelen Voss",
                title: "Signals Intelligence & Brig Warden",
                faction: "Iron Ridge PMC",
                faction_badge: "[PMC BRIG]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[CAPTURED POW]",
                emotion: "NORMAL",
                text: "Commander {PLAYER_CALLSIGN}. The hostile pilot recovered from the battlefield ejection pod is conscious in Cell 03. Medical scans indicate moderate G-force concussion, but neuro-synaptic telemetry confirms an elite ace with over a dozen confirmed warframe kills. They are refusing standard identification."
            },
            {
                layout: "DUAL",
                active_side: "RIGHT",
                speaker: "Captured Faction Ace",
                title: "Downed Strike Flight Leader",
                faction: "Captured Hostile Forces",
                faction_badge: "[PMC BRIG]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[CAPTURED POW]",
                emotion: "ANGRY",
                text: "Save your interrogation scripts, mercenary! I saw the registration codes on your ironclads. You're scavengers fighting for bank accounts. Put me in front of a firing squad or keep me locked in this cage, but you will not get one word of tactical cipher from me!"
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Intelligence Officer Kaelen Voss",
                title: "Signals Intelligence & Brig Warden",
                faction: "Iron Ridge PMC",
                faction_badge: "[PMC BRIG]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[CAPTURED POW]",
                emotion: "CALCULATING",
                text: "Their home government has already marked their ejection transponder as 'K.I.A.' to avoid paying family survivorship pensions. We hold all the cards, Commander. How shall we process the prisoner?"
            },
            {
                layout: "DUAL",
                active_side: "LEFT",
                speaker: "Tactical War Room // Interrogation Terminal",
                title: "Detention Command",
                faction: "POW Triage Protocol",
                faction_badge: "[TRIAGE DECISION]",
                portrait: spr_portrait_commander_male,
                portrait_right: spr_portrait_commander_female,
                faction_badge_right: "[PRISONER CELL]",
                emotion: "NORMAL",
                text: "The prisoner awaits your command. Will you offer a mercenary commission, extract enemy chassis telemetry, or arrange a diplomatic exchange?",
                choices: [
                    {
                        text: "Mercenary Commission: Offer upfront signing bonus and ship berth in our active squadron.",
                        pillar: "RECRUITMENT // REDEMPTION",
                        impact_label: "Recruit Ace Pilot | -25,000 Cr Bonus | +Noble Karma",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(-25000);
                                if (variable_struct_exists(obj_GameManager, "pmc_karma_noble")) obj_GameManager.pmc_karma_noble += 15;
                                if (variable_struct_exists(obj_GameManager.facilities, "roster_pilots")) {
                                    var _rec_ace = {
                                        id: "recruited_pow_" + string(irandom(9999)),
                                        name: "Lt. Kara Vane",
                                        callsign: "Valkyrie-6",
                                        rank: "Ace Veteran",
                                        combat_stat: 8,
                                        tactics_stat: 7,
                                        accuracy: 86,
                                        reflexes: 82,
                                        salary_daily: 95,
                                        current_mech_id: "",
                                        affinity: "ironclad",
                                        rank_perks: ["Deadly Aim", "Vernier Drift"],
                                        status: "READY",
                                        sorties_flown: 0,
                                        kills: 0,
                                        xp: 450,
                                        level: 2
                                    };
                                    array_push(obj_GameManager.facilities.roster_pilots, _rec_ace);
                                }
                            }
                            if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("POW RECRUITED: Kara Vane [Valkyrie-6] joined the Active Squadron!", c_lime);
                        }
                    },
                    {
                        text: "Coerce Blueprint Telemetry: Extract flight recorder encryption and chassis specs.",
                        pillar: "TECH EXTRACTION // SINTERING TELEMETRY",
                        impact_label: "+35,000 Cr Intel Bounty | +20 Tungsten | +Pragmatist Karma",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(35000);
                                obj_GameManager.add_raw_material("mat_tungsten", 20);
                                if (variable_struct_exists(obj_GameManager, "pmc_karma_pragmatist")) obj_GameManager.pmc_karma_pragmatist += 15;
                            }
                            if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("TELEMETRY EXTRACTED: +35,000 Cr & +20x Tungsten from prisoner flight log!", c_yellow);
                        }
                    },
                    {
                        text: "Diplomatic Prisoner Exchange: Arrange formal ransom transfer with home faction.",
                        pillar: "DIPLOMACY // RANSOM EXCHANGE",
                        impact_label: "+45,000 Cr Ransom | +15 Faction Standing | +Noble Karma",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(45000);
                                if (variable_struct_exists(obj_GameManager, "pmc_karma_noble")) obj_GameManager.pmc_karma_noble += 15;
                            }
                            if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_a", 15);
                            if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("PRISONER EXCHANGED: +45,000 Cr Ransom & +15 Coalition Standing!", c_aqua);
                        }
                    }
                ]
            }
        ]
    };

    // --- 2. CANTINA BOND: LT. GREGORY VANCE ---
    global.vn_state.episodes[$ "ep_cantina_bond_vance"] = {
        title: "OFFICERS' MESS // LT. GREGORY VANCE'S VIGIL",
        bg_scene: spr_loc_hangar_bay,
        nodes: [
            {
                layout: "SOLO",
                active_side: "LEFT",
                speaker: "Lt. Gregory Vance",
                title: "Tactical Executive Officer & Lead Wingman",
                faction: "Iron Ridge PMC",
                faction_badge: "[CREW BOND]",
                portrait: spr_portrait_commander_male,
                emotion: "DESPERATE",
                text: "Can't sleep, Commander {PLAYER_CALLSIGN}. I kept checking the gun-camera telemetry from our last clash. That Coalition strike wing we neutralized... the lead ironclad was flying the 14th Heavy Armor division crest. That was my old squadron. Three years ago, we were celebrating commission trials together on the Moon. Out here, we're tearing each other apart with railguns for credit bounties."
            },
            {
                layout: "SOLO",
                active_side: "LEFT",
                speaker: "Lt. Gregory Vance",
                title: "Tactical Executive Officer & Lead Wingman",
                faction: "Iron Ridge PMC",
                faction_badge: "[CREW BOND]",
                portrait: spr_portrait_commander_male,
                emotion: "NORMAL",
                text: "I believe in what Iron Ridge is building, Commander. But sometimes in the cockpit, when the target bracket locks onto an Earth Coalition transponder... my finger hesitates on the trigger. How do you live with it?"
            },
            {
                layout: "SOLO",
                active_side: "LEFT",
                speaker: "Officers' Mess // Personal Terminal",
                title: "Commander's Counsel",
                faction: "Crew Bond Decision",
                faction_badge: "[BOND COUNSEL]",
                portrait: spr_portrait_commander_male,
                emotion: "NORMAL",
                text: "Your guidance will shape Lt. Vance's combat philosophy and unlock a unique Squadron Synergy Perk.",
                choices: [
                    {
                        text: "Brothers in Arms: 'We fight for each other, Gregory. To keep this crew alive.'",
                        pillar: "LOYALTY // CAMARADERIE",
                        impact_label: "Unlocks Perk: Brothers in Arms (+5% Tandem Volley Accuracy)",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                if (!variable_struct_exists(obj_GameManager, "squadron_perks")) obj_GameManager.squadron_perks = [];
                                array_push(obj_GameManager.squadron_perks, "Brothers in Arms");
                            }
                            if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("CREW BOND RATIFIED: Lt. Vance unlocked [Brothers in Arms] (+5% ACC)!", c_lime);
                        }
                    },
                    {
                        text: "Righteous Fury: 'The Coalition high command threw you away. Fight for the new dawn.'",
                        pillar: "VENGEANCE // REVOLUTION",
                        impact_label: "Unlocks Perk: Righteous Fury (+10% Critical Kinetic Damage)",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                if (!variable_struct_exists(obj_GameManager, "squadron_perks")) obj_GameManager.squadron_perks = [];
                                array_push(obj_GameManager.squadron_perks, "Righteous Fury");
                            }
                            if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("CREW BOND RATIFIED: Lt. Vance unlocked [Righteous Fury] (+10% Crit DMG)!", c_orange);
                        }
                    }
                ]
            }
        ]
    };

    // --- 3. CANTINA BOND: DR. ANIKA SOREN ---
    global.vn_state.episodes[$ "ep_cantina_bond_soren"] = {
        title: "MEDICAL BAY // DR. ANIKA SOREN'S PROTOCOL",
        bg_scene: spr_loc_hangar_bay,
        nodes: [
            {
                layout: "SOLO",
                active_side: "LEFT",
                speaker: "Dr. Anika Soren",
                title: "Chief Medical Officer // Neuro-Cybernetics",
                faction: "Iron Ridge PMC",
                faction_badge: "[CREW BOND]",
                portrait: spr_portrait_commander_female,
                emotion: "NORMAL",
                text: "Commander {PLAYER_CALLSIGN}. Review these electro-encephalogram readouts from our cockpit pods. Whenever our pilots engage vernier drift or aimed limb targeting, their synthetic neuro-links experience extreme voltage spikes. Left unchecked, cockpit shock leads to permanent motor degradation."
            },
            {
                layout: "SOLO",
                active_side: "LEFT",
                speaker: "Dr. Anika Soren",
                title: "Chief Medical Officer // Neuro-Cybernetics",
                faction: "Iron Ridge PMC",
                faction_badge: "[CREW BOND]",
                portrait: spr_portrait_commander_female,
                emotion: "SMUG",
                text: "I have formulated an advanced neuro-inhibitor flush. If you authorize thirty thousand credits to install automated dialysis filters into our medical convalescence tanks, we can stabilize pilot trauma and reduce ICU recovery times by 25% across the entire squadron."
            },
            {
                layout: "SOLO",
                active_side: "LEFT",
                speaker: "Medical Bay // Protocol Terminal",
                title: "Convalescence Upgrade",
                faction: "Medical Decision",
                faction_badge: "[MEDICAL UPGRADE]",
                portrait: spr_portrait_commander_female,
                emotion: "NORMAL",
                text: "Will you fund Dr. Soren's automated neuro-inhibitor flush protocol?",
                choices: [
                    {
                        text: "Authorize Medical Flush: Install dialysis filters (-30,000 Credits).",
                        pillar: "PILOT WELFARE // CONVALESCENCE",
                        impact_label: "Unlocks: Combat Triage Protocol (-25% ICU Recovery Days)",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_funds(-30000);
                                if (!variable_struct_exists(obj_GameManager, "squadron_perks")) obj_GameManager.squadron_perks = [];
                                array_push(obj_GameManager.squadron_perks, "Combat Triage Protocol");
                            }
                            if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("MEDICAL UPGRADE: Combat Triage Protocol Active (-25% ICU Days)!", c_aqua);
                        }
                    },
                    {
                        text: "Rely on Conventional Stimulants: Conserve funds for frame manufacturing.",
                        pillar: "FISCAL RESTRAINT // STANDARD CARE",
                        impact_label: "Zero Credit Cost | Convalescence Times Unchanged",
                        action: function() {
                            // No change
                        }
                    }
                ]
            }
        ]
    };

    // --- 4. CANTINA BOND: CHIEF MARCUS KOVACS ---
    global.vn_state.episodes[$ "ep_cantina_bond_kovacs"] = {
        title: "FOUNDRY CRUCIBLE // CHIEF KOVACS' MASTERWORK",
        bg_scene: spr_loc_hangar_bay,
        nodes: [
            {
                layout: "SOLO",
                active_side: "LEFT",
                speaker: "Chief Marcus Kovacs",
                title: "Foundry Master // Flagship Engineering",
                faction: "Iron Ridge PMC",
                faction_badge: "[CREW BOND]",
                portrait: spr_portrait_commander_male,
                emotion: "SMUG",
                text: "Commander! Listen to that crucible roar! We just finished quenching our third batch of high-purity Titanium-Carbide. But here's the real breakthrough: I've discovered a way to overclock our mobile suit hydraulic actuators during launch cat-shots. If you spare five canisters of Syn-Flux, I can inject a high-octane catalyst that grants every deployed mech +1 Action Point on the opening round of combat!"
            },
            {
                layout: "SOLO",
                active_side: "LEFT",
                speaker: "Foundry Master // Tuning Terminal",
                title: "Actuator Calibration",
                faction: "Engineering Decision",
                faction_badge: "[CRUCIBLE TUNING]",
                portrait: spr_portrait_commander_male,
                emotion: "NORMAL",
                text: "Will you allocate 5 units of Syn-Flux to overclock squadron hydraulic actuators?",
                choices: [
                    {
                        text: "Authorize Actuator Overclock: Allocate 5x Syn-Flux to the crucible.",
                        pillar: "ENGINEERING EXCELLENCE // TACTICAL SPEED",
                        impact_label: "Unlocks: Overclocked Actuators (+1 Action Point on Turn 1 in all battles)",
                        action: function() {
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.add_raw_material("mat_syn_flux", -5);
                                if (!variable_struct_exists(obj_GameManager, "squadron_perks")) obj_GameManager.squadron_perks = [];
                                array_push(obj_GameManager.squadron_perks, "Overclocked Actuators");
                            }
                            if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("FOUNDRY MASTERWORK: [Overclocked Actuators] (+1 AP on Turn 1) Active!", c_lime);
                        }
                    },
                    {
                        text: "Preserve Syn-Flux: Keep all chemical flux for prototype component forging.",
                        pillar: "RESOURCE CONSERVATION",
                        impact_label: "Zero Material Cost | Actuators Run at Factory Specs",
                        action: function() {
                            // No change
                        }
                    }
                ]
            }
        ]
    };

    // =========================================================================
    // FOUNDRY ACTIVATION PROLOGUE: USN-X HEPHAESTUS LINEAGE CALIBRATION
    // =========================================================================
    global.vn_state.episodes[$ "ep_foundry_calibration"] = {
        title: "FOUNDRY ACTIVATION // USN-X HEPHAESTUS CRUCIBLE CALIBRATION",
        bg_scene: spr_loc_hangar_bay,
        nodes: [
            {
                speaker: "Chief Engineer Jessica Vance",
                title: "Chief Foundry Architect // USN-X Hephaestus",
                faction: "PMC Vanguard Engineering",
                faction_badge: "[HEPHAESTUS FOUNDRY]",
                portrait: spr_portrait_vance,
                text: "Commander, the pre-war automated crucible aboard the Hephaestus is finally holding a stable plasma containment arc. Before we stamp our first mass-production frame, I need you to lock in our foundational chassis doctrine."
            },
            {
                speaker: "Chief Engineer Jessica Vance",
                title: "Chief Foundry Architect // USN-X Hephaestus",
                faction: "PMC Vanguard Engineering",
                faction_badge: "[HEPHAESTUS FOUNDRY]",
                portrait: spr_portrait_vance,
                text: "All three base frames roll off the gantry unarmed with standard modular hardpoint rails, then receive our Type-90 90mm Machine Gun, Type-1 Heat Axe, and Deflector Buckler. Which foundry lineage should we calibrate for the Vanguard?",
                choices: [
                    {
                        text: "Aegis Visor Doctrine (Medium Balanced Wanzer — 880 HP | 60T | 55 km/h)",
                        pillar: "LINEAGE 1 // AEGIS VISOR",
                        impact_label: "Sets Foundry Lineage: Aegis Visor + Starter Trio Kit",
                        action: function() {
                            if (instance_exists(obj_GameManager)) obj_GameManager.set_foundry_lineage(0);
                            if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("FOUNDRY CALIBRATED: [AEGIS VISOR DOCTRINE] + Starter Kit Ready!", c_aqua);
                        }
                    },
                    {
                        text: "Colossus Heavy Forge Doctrine (Industrial Dreadnought — 980 HP | 78T | 40 km/h)",
                        pillar: "LINEAGE 2 // COLOSSUS FORGE",
                        impact_label: "Sets Foundry Lineage: Colossus Heavy Forge + Starter Trio Kit",
                        action: function() {
                            if (instance_exists(obj_GameManager)) obj_GameManager.set_foundry_lineage(1);
                            if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("FOUNDRY CALIBRATED: [COLOSSUS HEAVY FORGE] + Starter Kit Ready!", make_color_rgb(255, 165, 40));
                        }
                    },
                    {
                        text: "Stratos Vector Doctrine (Light Agile Recon — 650 HP | 42T | 90 km/h)",
                        pillar: "LINEAGE 3 // STRATOS VECTOR",
                        impact_label: "Sets Foundry Lineage: Stratos Vector + Starter Trio Kit",
                        action: function() {
                            if (instance_exists(obj_GameManager)) obj_GameManager.set_foundry_lineage(2);
                            if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("FOUNDRY CALIBRATED: [STRATOS VECTOR DOCTRINE] + Starter Kit Ready!", c_lime);
                        }
                    }
                ]
            }
        ]
    };

}

function scr_vn_is_active() {
    return (variable_global_exists("vn_state") && is_struct(global.vn_state) && global.vn_state.active);
}

function scr_vn_start_episode(_ep_id) {
    if (!variable_global_exists("vn_state") || !is_struct(global.vn_state)) {
        scr_vn_init();
    }
    if (!variable_struct_exists(global.vn_state.episodes, _ep_id)) return false;

    global.vn_state.active = true;
    global.vn_state.episode_id = _ep_id;
    global.vn_state.step_idx = 0;
    global.vn_state.char_progress = 0;
    global.vn_state.last_tick_char = 0;
    scr_audio_play_ui("boot");
    return true;
}

function scr_vn_close() {
    if (variable_global_exists("vn_state") && is_struct(global.vn_state)) {
        var _cur_ep = global.vn_state.episode_id;
        global.vn_state.active = false;
        scr_audio_play_ui("cancel");
        if (_cur_ep == "ep_00_pirate_trap") {
            if (instance_exists(obj_HQTerminal)) {
                obj_HQTerminal.intro_active = false;
                obj_HQTerminal.show_commander_modal = false;
            }
            if (instance_exists(obj_GameManager)) {
                obj_GameManager.prologue_active = true;
                obj_GameManager.has_completed_dossier = true;
            }
            if (room_exists(rm_combat)) room_goto(rm_combat);
        }
    }
}

function scr_vn_draw(_mx, _my, _click) {
    if (!scr_vn_is_active()) return;

    var _ep = global.vn_state.episodes[$ global.vn_state.episode_id];
    if (is_undefined(_ep)) {
        global.vn_state.active = false;
        return;
    }

    var _nodes = _ep.nodes;
    var _cur_idx = global.vn_state.step_idx;
    if (_cur_idx >= array_length(_nodes)) {
        global.vn_state.active = false;
        return;
    }

    var _node = _nodes[_cur_idx];
    var _gw = display_get_gui_width();
    var _gh = display_get_gui_height();

    // 1. Full-Screen Dimmed Backdrop with Cinematic Letterboxing
    draw_set_color(c_black);
    draw_set_alpha(0.85);
    draw_rectangle(0, 0, _gw, _gh, false);
    draw_set_alpha(1.0);

    // Optional Background Illustration vignette
    if (variable_struct_exists(_ep, "bg_scene") && sprite_exists(_ep.bg_scene)) {
        draw_sprite_ext(_ep.bg_scene, 0, 0, 0, _gw / 1024.0, _gh / 576.0, 0, c_white, 0.22);
    }

    // Top Cinematic Episode Banner
    draw_set_color(make_color_rgb(14, 22, 34));
    draw_rectangle(0, 0, _gw, 42, false);
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_line(0, 42, _gw, 42);

    draw_set_color(make_color_rgb(100, 220, 255));
    draw_text(24, 12, _ep.title);

    // Top-right Close/Skip Button
    var _sk_w = 110;
    var _sk_h = 28;
    var _sk_x = _gw - _sk_w - 20;
    var _sk_y = 7;
    var _sk_hov = (_mx >= _sk_x && _mx <= _sk_x + _sk_w && _my >= _sk_y && _my <= _sk_y + _sk_h);
    if (_sk_hov && _click) {
        scr_vn_close();
        return;
    }
    scr_draw_snes_button(_sk_x, _sk_y, _sk_w, _sk_h, "[ESC: CLOSE]", _sk_hov, false, make_color_rgb(220, 80, 80));

    // 2. Main Dialogue Frame (Bottom Panel)
    var _box_w = min(1100, _gw - 64);
    var _box_h = 240;
    var _box_x = (_gw - _box_w) / 2;
    var _box_y = _gh - _box_h - 28;

    // Panel Outer Bezel
    draw_set_color(make_color_rgb(10, 16, 26));
    draw_rectangle(_box_x, _box_y, _box_x + _box_w, _box_y + _box_h, false);
    draw_set_color(make_color_rgb(0, 210, 255));
    draw_rectangle(_box_x, _box_y, _box_x + _box_w, _box_y + _box_h, true);
    draw_set_color(make_color_rgb(20, 45, 75));
    draw_rectangle(_box_x + 3, _box_y + 3, _box_x + _box_w - 3, _box_y + _box_h - 3, true);

    // 3. Speaker Portrait Layout (Doc 52 Dual & Single Layout Support)
    var _is_dual = (variable_struct_exists(_node, "portrait_right") && sprite_exists(_node.portrait_right));
    var _side = (variable_struct_exists(_node, "active_side") ? _node.active_side : "LEFT");
    var _p_size = _is_dual ? 136 : 148;
    var _p_x = _box_x + 18;
    var _p_y = _box_y + 20;

    // Left Speaker Box & Emotion Shader (Doc 53)
    var _emo = variable_struct_exists(_node, "emotion") ? _node.emotion : "NORMAL";
    var _emo_col = make_color_rgb(0, 240, 255);
    var _emo_tag = "[RESOLUTE]";
    if (_emo == "ANGRY" || _emo == "BELLIGERENT") {
        _emo_col = make_color_rgb(255, 60, 60);
        _emo_tag = "[ENRAGED]";
    } else if (_emo == "DESPERATE" || _emo == "ALARMED") {
        _emo_col = (current_time mod 300 < 150) ? make_color_rgb(255, 180, 40) : make_color_rgb(220, 80, 20);
        _emo_tag = "[CRITICAL]";
    } else if (_emo == "SMUG" || _emo == "CALCULATING") {
        _emo_col = make_color_rgb(255, 215, 80);
        _emo_tag = "[CALCULATING]";
    }

    draw_set_color(make_color_rgb(16, 24, 38));
    draw_rectangle(_p_x, _p_y, _p_x + _p_size, _p_y + _p_size, false);

    var _left_alpha = (_is_dual && _side != "LEFT") ? 0.40 : 1.0;
    var _left_border = (_is_dual && _side != "LEFT") ? make_color_rgb(45, 65, 85) : _emo_col;

    if (variable_struct_exists(_node, "portrait") && sprite_exists(_node.portrait)) {
        draw_sprite_ext(_node.portrait, 0, _p_x, _p_y, _p_size / 200.0, _p_size / 200.0, 0, c_white, _left_alpha);
    }
    draw_set_color(_left_border);
    draw_rectangle(_p_x, _p_y, _p_x + _p_size, _p_y + _p_size, true);

    // Left Faction & Emotion Ribbons
    draw_set_color(make_color_rgb(24, 48, 80));
    draw_rectangle(_p_x, _p_y + _p_size + 6, _p_x + _p_size, _p_y + _p_size + 24, false);
    draw_set_color((_is_dual && _side != "LEFT") ? make_color_rgb(100, 140, 180) : make_color_rgb(120, 220, 255));
    draw_text_transformed(_p_x + 6, _p_y + _p_size + 9, _node.faction_badge, 0.70, 0.70, 0);

    // Emotion State Tag
    if (!_is_dual || _side == "LEFT") {
        draw_set_color(_emo_col);
        draw_text_transformed(_p_x + 6, _p_y + 6, _emo_tag, 0.65, 0.65, 0);
    }

    // 3b. Optional Right Speaker Box (Dual Layout)
    if (_is_dual) {
        var _pr_x = _box_x + _box_w - _p_size - 18;
        var _pr_y = _box_y + 20;
        var _right_alpha = (_side == "RIGHT") ? 1.0 : 0.40;
        var _right_border = (_side == "RIGHT") ? make_color_rgb(255, 215, 80) : make_color_rgb(45, 65, 85);

        draw_set_color(make_color_rgb(16, 24, 38));
        draw_rectangle(_pr_x, _pr_y, _pr_x + _p_size, _pr_y + _p_size, false);

        draw_sprite_ext(_node.portrait_right, 0, _pr_x, _pr_y, _p_size / 200.0, _p_size / 200.0, 0, c_white, _right_alpha);
        draw_set_color(_right_border);
        draw_rectangle(_pr_x, _pr_y, _pr_x + _p_size, _pr_y + _p_size, true);

        // Right Faction Ribbon
        draw_set_color(make_color_rgb(24, 48, 80));
        draw_rectangle(_pr_x, _pr_y + _p_size + 6, _pr_x + _p_size, _pr_y + _p_size + 24, false);
        var _r_badge = variable_struct_exists(_node, "faction_badge_right") ? _node.faction_badge_right : "[RIVAL]";
        draw_set_color((_side == "RIGHT") ? make_color_rgb(255, 220, 120) : make_color_rgb(100, 140, 180));
        draw_text_transformed(_pr_x + 6, _pr_y + _p_size + 9, _r_badge, 0.70, 0.70, 0);
    }

    // 4. Speaker Nameplate & Title Banner
    var _txt_x = _p_x + _p_size + 22;
    var _txt_w = _is_dual ? (_box_w - (2 * _p_size + 76)) : (_box_w - (_p_size + 60));

    draw_set_color((_is_dual && _side == "RIGHT") ? make_color_rgb(255, 215, 80) : make_color_rgb(255, 220, 90));
    draw_text_transformed(_txt_x, _box_y + 16, _node.speaker, 1.05, 1.05, 0);

    draw_set_color(make_color_rgb(140, 185, 225));
    draw_text_transformed(_txt_x, _box_y + 38, _node.title + " // " + _node.faction, 0.75, 0.75, 0);

    draw_set_color(make_color_rgb(40, 75, 115));
    draw_line(_txt_x, _box_y + 54, _txt_x + _txt_w, _box_y + 54);

    // 5. Typewriter Dialogue Display with Interpolation (Doc 52)
    var _full_text = scr_vn_interpolate_text(_node.text);
    var _full_len = string_length(_full_text);

    if (global.vn_state.char_progress < _full_len) {
        global.vn_state.char_progress = min(_full_len, global.vn_state.char_progress + global.vn_state.typewriter_speed);
        if (floor(global.vn_state.char_progress) > global.vn_state.last_tick_char) {
            global.vn_state.last_tick_char = floor(global.vn_state.char_progress);
            if (global.vn_state.last_tick_char % 4 == 0) {
                scr_audio_play_ui("click");
            }
        }
    }

    var _display_len = floor(global.vn_state.char_progress);
    var _partial_text = string_copy(_full_text, 1, _display_len);

    draw_set_color(make_color_rgb(220, 240, 255));
    draw_text_ext_transformed(_txt_x, _box_y + 64, _partial_text, 22, floor(_txt_w / 0.92), 0.92, 0.92, 0);

    var _text_is_complete = (_display_len >= _full_len);
    var _has_choices = (variable_struct_exists(_node, "choices") && is_array(_node.choices) && array_length(_node.choices) > 0);

    // 6. Tri-Pillar Interactive Choice Cards or Advance Prompt
    if (!_has_choices) {
        // Simple Advance Prompt
        var _prompt_pulse = 0.5 + 0.5 * sin(current_time * 0.008);
        draw_set_color(merge_color(make_color_rgb(100, 200, 255), c_white, _prompt_pulse));
        var _adv_str = (_cur_idx < array_length(_nodes) - 1) ? "[ CLICK OR PRESS SPACE TO ADVANCE >> ]" : "[ CLICK TO CONCLUDE BRIEFING >> ]";
        draw_text_transformed(_txt_x + _txt_w - 280, _box_y + _box_h - 26, _adv_str, 0.78, 0.78, 0);

        if (_click || keyboard_check_pressed(vk_space) || keyboard_check_pressed(vk_enter)) {
            if (!_text_is_complete) {
                global.vn_state.char_progress = _full_len;
            } else {
                global.vn_state.step_idx++;
                global.vn_state.char_progress = 0;
                global.vn_state.last_tick_char = 0;
                scr_audio_play_ui("click");
                if (global.vn_state.step_idx >= array_length(_nodes)) {
                    global.vn_state.active = false;
                }
            }
        }
    } else {
        // Render 3 Choice Options
        if (!_text_is_complete) {
            // Click to skip typewriter to full choices
            if (_click || keyboard_check_pressed(vk_space)) {
                global.vn_state.char_progress = _full_len;
            }
        } else {
            var _choices = _node.choices;
            var _c_count = array_length(_choices);
            var _ch_y0 = _box_y + 118;
            var _ch_h = min(32, floor((_box_h - 110) / max(1, _c_count)) - 4);

            for (var c = 0; c < _c_count; c++) {
                var _ch = _choices[c];
                var _ch_y = _ch_y0 + c * (_ch_h + 6);
                var _ch_hov = (_mx >= _txt_x && _mx <= _txt_x + _txt_w && _my >= _ch_y && _my <= _ch_y + _ch_h);

                if (_ch_hov && _click) {
                    if (is_method(_ch.action)) {
                        _ch.action();
                    }
                    scr_audio_play_ui("confirm");
                    global.vn_state.step_idx++;
                    global.vn_state.char_progress = 0;
                    global.vn_state.last_tick_char = 0;
                    if (global.vn_state.step_idx >= array_length(_nodes)) {
                        global.vn_state.active = false;
                    }
                    return;
                }

                draw_set_color(_ch_hov ? make_color_rgb(26, 60, 95) : make_color_rgb(14, 22, 34));
                draw_rectangle(_txt_x, _ch_y, _txt_x + _txt_w, _ch_y + _ch_h, false);
                draw_set_color(_ch_hov ? make_color_rgb(60, 240, 140) : make_color_rgb(45, 85, 130));
                draw_rectangle(_txt_x, _ch_y, _txt_x + _txt_w, _ch_y + _ch_h, true);

                // Pillar Tag
                draw_set_color(_ch_hov ? make_color_rgb(255, 230, 100) : make_color_rgb(0, 210, 255));
                draw_text_transformed(_txt_x + 10, _ch_y + 4, "[" + _ch.pillar + "]", 0.72, 0.72, 0);

                // Choice Text
                draw_set_color(_ch_hov ? c_white : make_color_rgb(200, 225, 245));
                draw_text_transformed(_txt_x + 10, _ch_y + 17, _ch.text, 0.75, 0.75, 0);

                // Consequence Impact Badge (Right aligned)
                draw_set_color(_ch_hov ? make_color_rgb(100, 255, 180) : make_color_rgb(255, 200, 90));
                draw_text_transformed(_txt_x + _txt_w - 320, _ch_y + 10, _ch.impact_label, 0.68, 0.68, 0);
            }
        }
    }
}


// =============================================================================
// REACTIVE GEOPOLITICAL VN NOVEL SYSTEM (DOC 52)
// =============================================================================

/// @function scr_vn_interpolate_text(_raw_text)
/// @description Parses and replaces dynamic world state tokens ({PLAYER_CALLSIGN}, {RECENT_SECTOR}, {ROSTER_PILOT}, etc.)
function scr_vn_interpolate_text(_raw_text) {
    if (!is_string(_raw_text)) return "";
    var _txt = _raw_text;

    // Player Commander Callouts
    var _cmdr_callsign = "VANGUARD";
    var _cmdr_name = "Commander";
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "player_commander") && is_struct(obj_GameManager.player_commander)) {
        if (variable_struct_exists(obj_GameManager.player_commander, "callsign")) _cmdr_callsign = obj_GameManager.player_commander.callsign;
        if (variable_struct_exists(obj_GameManager.player_commander, "name")) _cmdr_name = obj_GameManager.player_commander.name;
    }
    _txt = string_replace_all(_txt, "{PLAYER_CALLSIGN}", _cmdr_callsign);
    _txt = string_replace_all(_txt, "{PLAYER_NAME}", _cmdr_name);

    // Recent Contested Sector Callout
    var _recent_sector = "Olympus Mons";
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "last_battle_report") && !is_undefined(obj_GameManager.last_battle_report)) {
        if (variable_struct_exists(obj_GameManager.last_battle_report, "sector_name")) {
            _recent_sector = obj_GameManager.last_battle_report.sector_name;
        }
    }
    _txt = string_replace_all(_txt, "{RECENT_SECTOR}", _recent_sector);

    // Lead Roster Pilot Callout
    var _roster_pilot = "Lt. Sonya Cruz";
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "facilities") && is_struct(obj_GameManager.facilities)) {
        if (variable_struct_exists(obj_GameManager.facilities, "roster_pilots") && is_array(obj_GameManager.facilities.roster_pilots)) {
            var _rp = obj_GameManager.facilities.roster_pilots;
            if (array_length(_rp) > 0) {
                _roster_pilot = _rp[0].name + " ('" + _rp[0].callsign + "')";
            }
        }
    }
    _txt = string_replace_all(_txt, "{ROSTER_PILOT}", _roster_pilot);

    // Brig Incarcerated Prisoner Callout
    var _brig_prisoner = "Captured Hyena Ace";
    if (instance_exists(obj_NemesisManager) && variable_instance_exists(obj_NemesisManager, "prisoner_list") && is_array(obj_NemesisManager.prisoner_list)) {
        var _pl = obj_NemesisManager.prisoner_list;
        if (array_length(_pl) > 0) {
            _brig_prisoner = _pl[0].name;
        }
    }
    _txt = string_replace_all(_txt, "{BRIG_PRISONER}", _brig_prisoner);

    // Flagship Callout
    _txt = string_replace_all(_txt, "{FLAGSHIP}", "USN-X Hephaestus");

    return _txt;
}

/// @function scr_vn_start_dynamic_audience(_faction_id)
/// @description Assembles and starts a reactive 3-node VN audience with the leader based on standing, AI mood, and deeds.
function scr_vn_start_dynamic_audience(_faction_id) {
    if (!variable_global_exists("vn_state") || !is_struct(global.vn_state)) {
        scr_vn_init();
    }

    var _fm = instance_exists(obj_FactionManager) ? obj_FactionManager : undefined;
    var _standing = 0;
    var _ai_state = "PEACE";
    var _f_name = "Faction Command";
    var _speaker = "Diplomatic Attaché";
    var _title = "Liaison Officer";
    var _portrait = spr_portrait_commander_male;
    var _badge = "[DIPLOMACY]";
    var _primary_enemy = "faction_b";

    if (!is_undefined(_fm) && variable_struct_exists(_fm.factions, _faction_id)) {
        var _finfo = _fm.factions[$ _faction_id];
        _standing = _fm.get_standing(_faction_id);
        _ai_state = variable_struct_get(_finfo, "ai_state") ?? "PEACE";
        _f_name = _finfo.name;
        _primary_enemy = variable_struct_get(_finfo, "primary_enemy_id") ?? "faction_b";
    }

    if (_faction_id == "faction_a") {
        _speaker = "General Arthur Bradley";
        _title = "Supreme Commander // Earth Defense Front";
        _portrait = spr_portrait_commander_male;
        _badge = "[TERRAN COALITION]";
    } else if (_faction_id == "faction_b") {
        _speaker = "Commander Joshua Reed";
        _title = "Supreme Marshal // Outer Colony League";
        _portrait = spr_portrait_commander_female;
        _badge = "[COLONY LEAGUE]";
    } else if (_faction_id == "faction_c") {
        _speaker = "Captain Sonya Cruz";
        _title = "High Commodore // Corsair Syndicate";
        _portrait = spr_portrait_cruz;
        _badge = "[ROGUE SYNDICATE]";
    } else if (_faction_id == "faction_d") {
        _speaker = "Director Kenjiro Sato";
        _title = "Chief Executive Officer // Sato Heavy Industries";
        _portrait = spr_portrait_commander_silhouette;
        _badge = "[APEX ZAIBATSU]";
    } else if (_faction_id == "faction_e") {
        _speaker = "Archon Orin Sideris";
        _title = "First Sovereign // Republic Cylinder Astraea-01";
        _portrait = (sprite_exists(spr_portrait_sorren) ? spr_portrait_sorren : spr_portrait_commander_silhouette);
        _badge = "[SIDEREAL LEAGUE]";
    } else if (_faction_id == "faction_f") {
        _speaker = "Consensus Node 0-Prime";
        _title = "Deus Logica // Subterranean Red Crypt of Mars";
        _portrait = (sprite_exists(spr_portrait_null07) ? spr_portrait_null07 : spr_portrait_commander_silhouette);
        _badge = "[THARSIS CONSENSUS]";
    }

    // Node 0: Dynamic Mood Salutation
    var _mood_text = "";
    if (_standing <= -25) {
        _mood_text = "You dare establish an encrypted quantum uplink after declaring war on our sovereignty, {PLAYER_CALLSIGN}? Your mercenary syndicate is classified as a hostile belligerent. Speak your terms quickly before our orbital fire batteries lock your transmission source.";
    } else if (_ai_state == "DESPERATE") {
        _mood_text = "Commander {PLAYER_CALLSIGN}! Thank the stars you answered this frequency. Our frontline perimeter in {RECENT_SECTOR} is collapsing under saturation bombardment! If your Mobile Suits do not deploy immediately, our forces will be overrun. We will pay double standard contract rates!";
    } else if (_ai_state == "WINNING" || _standing >= 40) {
        _mood_text = "Greetings, Commander. The strategic war map is bending decisively toward our doctrine. The " + _f_name + " values our alliance with Iron Ridge. We are prepared to grant priority access to our military supply foundries.";
    } else if (_ai_state == "STANDARD_WAR") {
        _mood_text = "Uplink confirmed. Our battlegroups are actively engaged across all three operational theaters. We have no leisure for diplomatic pleasantries, Commander—we require immediate armored firepower on the frontlines.";
    } else {
        _mood_text = "Quantum link established with the " + _f_name + ". The commercial ledger between our commands remains open, Commander. State your operational availability and terms.";
    }

    // Node 1: Contextual Incident Bark
    var _incident_text = "";
    if (_standing < -10) {
        _incident_text = "Our strategic reconnaissance confirms that {ROSTER_PILOT} spearheaded the assault against our supply grid. Every kinetic slug fired by Iron Ridge is logged in our retaliation matrices. If you seek to de-escalate tensions, it will require immense commercial restitution.";
    } else if (_standing >= 20) {
        _incident_text = "Battlefield telemetry from {RECENT_SECTOR} confirms your squad's absolute tactical dominance. The " + _f_name + " recognizes discipline and lethal precision. We want your Mobile Suits under exclusive retainer.";
    } else {
        _incident_text = "Our logistical offices note that your flagship {FLAGSHIP} has unsealed pre-war manufacturing crucibles. We are prepared to trade high-density metallurgy for your combat escort sorties.";
    }

    // Determine dynamic emotion state (Doc 53)
    var _dynamic_emo = "NORMAL";
    if (_standing <= -25) _dynamic_emo = "ANGRY";
    else if (_ai_state == "DESPERATE") _dynamic_emo = "DESPERATE";
    else if (_ai_state == "WINNING" || _standing >= 40) _dynamic_emo = "SMUG";

    // Node 2: Consequential Strategic Choice
    var _nodes = [
        {
            speaker: _speaker,
            title: _title,
            faction: _f_name,
            faction_badge: _badge,
            portrait: _portrait,
            emotion: _dynamic_emo,
            text: _mood_text
        },
        {
            speaker: _speaker,
            title: _title,
            faction: _f_name,
            faction_badge: _badge,
            portrait: _portrait,
            emotion: (_dynamic_emo == "ANGRY" ? "ANGRY" : "NORMAL"),
            text: _incident_text
        },
        {
            speaker: _speaker,
            title: _title,
            faction: _f_name,
            faction_badge: _badge,
            portrait: _portrait,
            emotion: (_dynamic_emo == "DESPERATE" ? "DESPERATE" : "NORMAL"),
            text: "Here is our active diplomatic proposal. What is your response, Commander?",
            choices: [
                {
                    text: "Accept Frontline Contract: Deploy Mobile Suits in direct support.",
                    pillar: "ALLIANCE // STRATEGIC PACT",
                    impact_label: "+15 Standing | -10 Rival | +50,000 Cr Operational Retainer",
                    action: method({ fid: _faction_id, pen: _primary_enemy }, function() {
                        if (instance_exists(obj_FactionManager)) {
                            obj_FactionManager.modify_standing(fid, 15);
                            obj_FactionManager.modify_standing(pen, -10);
                        }
                        if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(50000);
                    })
                },
                {
                    text: "Metallurgical Exchange: Trade tactical telemetry for rare elements.",
                    pillar: "COMMERCE // RAW LOGISTICS",
                    impact_label: "+10 Standing | +20x Titanium | +15x Tungsten Ores",
                    action: method({ fid: _faction_id }, function() {
                        if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing(fid, 10);
                        if (instance_exists(obj_GameManager)) {
                            obj_GameManager.add_raw_material("mat_titanium", 20);
                            obj_GameManager.add_raw_material("mat_tungsten", 15);
                        }
                    })
                },
                {
                    text: "Defiant Rejection: Extort ransom or sever diplomatic ties.",
                    pillar: "EXTORTION // MERCENARY DEFIANCE",
                    impact_label: "-15 Standing | +10 Rival Standing | +65,000 Cr Black Market",
                    action: method({ fid: _faction_id, pen: _primary_enemy }, function() {
                        if (instance_exists(obj_FactionManager)) {
                            obj_FactionManager.modify_standing(fid, -15);
                            obj_FactionManager.modify_standing(pen, 10);
                        }
                        if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(65000);
                    })
                }
            ]
        }
    ];

    global.vn_state.episodes[$ "ep_dynamic_audience"] = {
        title: "DIPLOMATIC AUDIENCE // " + string_upper(_f_name),
        bg_scene: spr_loc_war_room,
        nodes: _nodes
    };

    return scr_vn_start_episode("ep_dynamic_audience");
}

/// @function scr_vn_trigger_combat_intercom(_speaker, _portrait, _text, _duration, _color, _directives)
/// @description Displays an in-combat Front Mission tactical radio squelch comms banner in rm_combat, optionally with clickable directives.
function scr_vn_trigger_combat_intercom(_speaker, _portrait, _text, _duration = 180, _color = c_lime, _directives = undefined) {
    if (!variable_global_exists("combat_intercom") || !is_struct(global.combat_intercom)) {
        global.combat_intercom = {
            active: false,
            speaker: "",
            portrait: -1,
            text: "",
            timer: 0,
            max_timer: 180,
            color: c_white,
            directives: undefined
        };
    }
    global.combat_intercom.active = true;
    global.combat_intercom.speaker = _speaker;
    global.combat_intercom.portrait = _portrait;
    global.combat_intercom.text = _text;
    global.combat_intercom.timer = (is_array(_directives) && array_length(_directives) > 0) ? 99999 : _duration;
    global.combat_intercom.max_timer = global.combat_intercom.timer;
    global.combat_intercom.color = _color;
    global.combat_intercom.directives = _directives;
    scr_audio_play_ui("boot");
}

/// @function scr_vn_draw_combat_intercom()
/// @description Draws the tactical military radio intercom banner on screen during combat, supporting interactive directive cards.
function scr_vn_draw_combat_intercom() {
    if (!variable_global_exists("combat_intercom") || !is_struct(global.combat_intercom) || !global.combat_intercom.active) return;
    
    var _ci = global.combat_intercom;
    var _has_dirs = (variable_struct_exists(_ci, "directives") && is_array(_ci.directives) && array_length(_ci.directives) > 0);
    
    if (!_has_dirs) {
        _ci.timer--;
        if (_ci.timer <= 0) {
            _ci.active = false;
            return;
        }
    }
    
    var _gw = display_get_gui_width();
    var _w = min(740, _gw - 80);
    var _h = _has_dirs ? 116 : 76;
    var _x = (_gw - _w) / 2;
    var _y = 54;
    
    var _alpha = (_ci.timer < 20) ? (_ci.timer / 20.0) : min(1.0, (_ci.max_timer - _ci.timer) / 10.0);
    draw_set_alpha(_alpha * 0.94);
    
    // Panel Background
    draw_set_color(make_color_rgb(10, 16, 24));
    draw_rectangle(_x, _y, _x + _w, _y + _h, false);
    
    // Border with blinking LED pulse
    var _blink = (current_time mod 300 < 150);
    draw_set_color(_ci.color);
    draw_rectangle(_x, _y, _x + _w, _y + _h, true);
    draw_set_color(make_color_rgb(25, 45, 65));
    draw_rectangle(_x + 2, _y + 2, _x + _w - 2, _y + _h - 2, true);
    
    // Portrait
    var _p_size = 56;
    var _px = _x + 10;
    var _py = _y + 10;
    draw_set_color(c_black);
    draw_rectangle(_px, _py, _px + _p_size, _py + _p_size, false);
    if (sprite_exists(_ci.portrait)) {
        draw_sprite_ext(_ci.portrait, 0, _px, _py, _p_size / 200.0, _p_size / 200.0, 0, c_white, _alpha);
    }
    draw_set_color(_ci.color);
    draw_rectangle(_px, _py, _px + _p_size, _py + _p_size, true);
    
    // Top Radio Frequency Banner
    draw_set_color(_blink ? make_color_rgb(80, 255, 120) : make_color_rgb(40, 180, 80));
    draw_text_transformed(_px + _p_size + 14, _y + 8, "[LIVE COMMS // CH-08 ENCRYPTED]", 0.68, 0.68, 0);
    
    // Speaker Name
    draw_set_color(make_color_rgb(255, 220, 90));
    draw_text_transformed(_px + _p_size + 14, _y + 22, _ci.speaker, 0.85, 0.85, 0);
    
    // Text
    draw_set_color(c_white);
    draw_text_ext_transformed(_px + _p_size + 14, _y + 38, _ci.text, 18, floor((_w - _p_size - 30) / 0.78), 0.78, 0.78, 0);
    
    // Directive Buttons
    if (_has_dirs) {
        var _mx = device_mouse_x_to_gui(0);
        var _my = device_mouse_y_to_gui(0);
        var _click = mouse_check_button_pressed(mb_left);
        var _dirs = _ci.directives;
        var _dc = array_length(_dirs);
        var _btn_w = floor((_w - 30) / max(1, _dc));
        var _btn_h = 28;
        var _btn_y = _y + _h - 36;
        
        for (var d = 0; d < _dc; d++) {
            var _dir = _dirs[d];
            var _bx = _x + 10 + d * (_btn_w + 5);
            var _b_hov = (_mx >= _bx && _mx <= _bx + _btn_w && _my >= _btn_y && _my <= _btn_y + _btn_h);
            
            if (_b_hov && _click) {
                if (is_method(_dir.action)) _dir.action();
                scr_audio_play_ui("confirm");
                _ci.active = false;
                _ci.directives = undefined;
                break;
            }
            
            draw_set_color(_b_hov ? make_color_rgb(30, 75, 115) : make_color_rgb(16, 28, 44));
            draw_rectangle(_bx, _btn_y, _bx + _btn_w, _btn_y + _btn_h, false);
            draw_set_color(_b_hov ? make_color_rgb(80, 240, 255) : make_color_rgb(45, 95, 140));
            draw_rectangle(_bx, _btn_y, _bx + _btn_w, _btn_y + _btn_h, true);
            draw_set_color(_b_hov ? c_white : make_color_rgb(200, 235, 255));
            draw_text_transformed(_bx + 6, _btn_y + 6, _dir.text, 0.72, 0.72, 0);
        }
    }
    
    draw_set_alpha(1.0);
}
