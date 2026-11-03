import re

fm_path = "objects/obj_FactionManager/Create_0.gml"
with open(fm_path, "r") as f:
    code = f.read()

# Update available_contracts with Era 0 starting contracts
old_cnt_marker = 'available_contracts = [\n    {\n        id: "cnt_terran_mass_01",'
new_cnt_block = '''available_contracts = [
    {
        id: "cnt_terran_convoy_01",
        faction: "faction_a",
        faction_name: "The Terran Coalition",
        type: "ESCORT_SORTIE",
        title: "OPERATION MAMMOTH ESCORT: TANK CONVOY DEFENSE",
        briefing: "Terran Coalition requires armored support to escort a supply convoy of T-720 Mammoth Battle Tanks through contested volcanic terrain.",
        required_tier: 1,
        required_quantity: 1,
        delivered_quantity: 0,
        payout_credits: 320000,
        reputation_gain: 15,
        reputation_penalty: -15,
        deadline_days: 25,
        days_remaining: 25,
        penalty_credits: 60000
    },
    {
        id: "cnt_colony_patrol_01",
        faction: "faction_b",
        faction_name: "The Outer Colonies",
        type: "INTERCEPTION_SORTIE",
        title: "SECTOR HARRIER: INTERCEPT SYNDICATE TECHNICALS",
        briefing: "Colony defense militia requests fast tactical interdiction against roving packs of pirate technicals threatening water mining claims.",
        required_tier: 1,
        required_quantity: 1,
        delivered_quantity: 0,
        payout_credits: 280000,
        reward_material_id: "mat_tritium",
        reward_material_amount: 5,
        reputation_gain: 20,
        reputation_penalty: -10,
        deadline_days: 18,
        days_remaining: 18,
        penalty_credits: 40000
    },
    {
        id: "cnt_syndicate_black_01",
        faction: "faction_c",
        faction_name: "Rogue Mercenary Syndicates",
        type: "BLACK_OPS_SALE",
        title: "BLACK MARKET RUN: EXPERIMENTAL TOKAMAK FLUX",
        briefing: "Smugglers will pay top dollar in refined Synthetic Flux for uncataloged magnetic containment rings. 35% Risk of Terran Intelligence leak!",
        required_tier: 1,
        required_quantity: 1,
        delivered_quantity: 0,
        payout_credits: 220000,
        reward_material_id: "mat_syn_flux",
        reward_material_amount: 8,
        tech_leak_risk_pct: 35,
        reputation_gain: 25,
        reputation_penalty: 0,
        deadline_days: 12,
        days_remaining: 12,
        penalty_credits: 0
    },
    {
        id: "cnt_zaibatsu_neural_01",
        faction: "faction_d",
        faction_name: "Apex Bio-Cybernetics Zaibatsu",
        type: "PROTOTYPE_BOUNTY",
        title: "PROJECT SUSANOO: NEURAL-SYNC HARMONIC CORE",
        briefing: "Director Renzo Takahashi requires an over-clocked Tokamak reactor core tuned to >=90% harmonic sync to field-test spinal neural-link interface latency.",
        required_tier: 2,
        required_quantity: 1,'''

if old_cnt_marker in code:
    idx = code.find(old_cnt_marker)
    # find where cnt_zaibatsu_neural_01 starts
    end_idx = code.find('    {\n        id: "cnt_zaibatsu_neural_01",', idx)
    if end_idx != -1:
        code = code[:idx] + new_cnt_block + code[end_idx + len('    {\n        id: "cnt_zaibatsu_neural_01",\n        faction: "faction_d",\n        faction_name: "Apex Bio-Cybernetics Zaibatsu",\n        type: "PROTOTYPE_BOUNTY",\n        title: "PROJECT SUSANOO: NEURAL-SYNC HARMONIC CORE",\n        briefing: "Director Renzo Takahashi requires an over-clocked Tokamak reactor core tuned to >=90% harmonic sync to field-test spinal neural-link interface latency.",\n        required_tier: 2,\n        required_quantity: 1,'):]
        print("Updated starting contracts to Era 0 conventional operations.")

# In on_mobile_suit_revolution, push the high-bounty tenders
rev_target = 'if (variable_struct_exists(territory_control, "last_shift_report")) {'
tenders_code = '''    // 2. Inject Urgent Prometheus High-Bounty Tenders
    array_push(available_contracts, {
        id: "cnt_prometheus_linebreaker_01",
        faction: "faction_a",
        faction_name: "The Terran Coalition",
        type: "PROMETHEUS_TENDER",
        title: "★ THE PROMETHEUS TENDER: BREAK THE TRENCH LINE ★",
        briefing: "Terran High Command offers an astronomical 3.0x bounty to deploy your bipedal Mobile Suit into Sector 4 to crush entrenched heavy tank battalions!",
        required_tier: 2,
        required_quantity: 1,
        delivered_quantity: 0,
        payout_credits: 750000,
        reward_material_id: "mat_tungsten",
        reward_material_amount: 50,
        reputation_gain: 30,
        reputation_penalty: -10,
        deadline_days: 35,
        days_remaining: 35,
        penalty_credits: 0
    });
    array_push(available_contracts, {
        id: "cnt_prometheus_colony_01",
        faction: "faction_b",
        faction_name: "The Outer Colonies",
        type: "PROMETHEUS_TENDER",
        title: "★ LIBERATION PACT: ORBITAL BEACHHEAD MOBILE SUIT DEFENSE ★",
        briefing: "Colonial Alliance requests Mobile Suit tactical superiority to shatter an incoming tank invasion force. Offers emergency Tritium reserves.",
        required_tier: 2,
        required_quantity: 1,
        delivered_quantity: 0,
        payout_credits: 680000,
        reward_material_id: "mat_tritium",
        reward_material_amount: 25,
        reputation_gain: 35,
        reputation_penalty: -15,
        deadline_days: 28,
        days_remaining: 28,
        penalty_credits: 0
    });

    ''' + rev_target

if rev_target in code and "cnt_prometheus_linebreaker_01" not in code:
    code = code.replace(rev_target, tenders_code)
    print("Injected Prometheus high-bounty tenders into on_mobile_suit_revolution.")

with open(fm_path, "w") as f:
    f.write(code)

print("obj_FactionManager contracts updated successfully.")
