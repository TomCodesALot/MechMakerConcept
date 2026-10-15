with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    content = f.read()

target = '''            // Sol Market Share Label ABOVE bar to ensure perfect contrast and zero text clipping
            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_rx, _ry + 20, "SOL SYSTEM MARKET SHARE RATIOS: VHI " + string(_rc.corp_vhi.market_share_pct) + "%  |  AOD " + string(_rc.corp_aod.market_share_pct) + "%  |  RUST " + string(_rc.corp_rust.market_share_pct) + "%  |  HATS " + string(_rc.corp_hats.market_share_pct) + "%  |  YOUR PMC: " + string(_gm.pmc_market_share_pct) + "%");

            // Sol Market Share Bar
            var _mbar_y = _ry + 38;'''

replacement = '''            // Timeline Tech Era Progression Banner (docs/27)
            var _era_y = _ry + 20;
            draw_set_color(make_color_rgb(14, 22, 32));
            draw_rectangle(_rx, _era_y, _rx + _rw, _era_y + 26, false);
            draw_set_color(make_color_rgb(45, 75, 110));
            draw_rectangle(_rx, _era_y, _rx + _rw, _era_y + 26, true);

            draw_set_color(make_color_rgb(255, 220, 100));
            draw_text(_rx + 12, _era_y + 5, "ACTIVE TIMELINE ERA: " + _gm.timeline_era_name + " (YEAR " + string(_gm.current_cycle_year) + " // DAY " + string(_gm.current_cycle_day) + ")");

            // 4 Segmented Era Status Indicators
            var _era_w = 110;
            var _era_labels = ["1. EARLY WAR", "2. ESCALATION", "3. TOTAL WAR", "4. APEX CRISIS"];
            for (var er = 0; er < 4; er++) {
                var _er_x = _rx + _rw - 475 + er * (_era_w + 6);
                var _is_cur = (_gm.timeline_era == (er + 1));
                var _is_past = (_gm.timeline_era > (er + 1));
                draw_set_color(_is_cur ? make_color_rgb(20, 60, 85) : (_is_past ? make_color_rgb(12, 36, 20) : make_color_rgb(12, 16, 22)));
                draw_rectangle(_er_x, _era_y + 3, _er_x + _era_w, _era_y + 23, false);
                draw_set_color(_is_cur ? make_color_rgb(100, 240, 255) : (_is_past ? c_lime : make_color_rgb(60, 80, 100)));
                draw_rectangle(_er_x, _era_y + 3, _er_x + _era_w, _era_y + 23, true);
                draw_text(_er_x + 6, _era_y + 5, _era_labels[er]);
            }

            // Sol Market Share Label ABOVE bar
            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_rx, _era_y + 32, "SOL SYSTEM MARKET SHARE RATIOS: VHI " + string(_rc.corp_vhi.market_share_pct) + "%  |  AOD " + string(_rc.corp_aod.market_share_pct) + "%  |  RUST " + string(_rc.corp_rust.market_share_pct) + "%  |  HATS " + string(_rc.corp_hats.market_share_pct) + "%  |  YOUR PMC: " + string(_gm.pmc_market_share_pct) + "%");

            // Sol Market Share Bar
            var _mbar_y = _era_y + 50;'''

if target in content:
    content = content.replace(target, replacement)
    print("Replaced market share bar with timeline era banner in Draw_64.gml")
else:
    print("ERROR: Target for timeline era banner not found!")

# Now update the corporate card details to show Procedural R&D Branch and X-Spec
target_card = '''                draw_set_color(make_color_rgb(170, 195, 220));
                draw_text(_cdx + 14, _cdy + 32, "CEO: " + _cp.ceo + "  |  HQ: " + _cp.hq_location);
                draw_text(_cdx + 14, _cdy + 52, "Faction Alignment: " + _cp.alignment);
                draw_text(_cdx + 14, _cdy + 72, "Core Specialty: " + _cp.specialty);
                draw_text(_cdx + 14, _cdy + 92, "Flagship Chassis: " + _cp.flagship_chassis);'''

replacement_card = '''                var _cp_cat = variable_struct_exists(_gm.competitor_catalog, _cid) ? _gm.competitor_catalog[$ _cid] : undefined;
                var _b_name = (!is_undefined(_cp_cat)) ? _cp_cat.branch_name : _cp.specialty;
                var _line_suit = (!is_undefined(_cp_cat) && !is_undefined(_cp_cat.active_line_chassis)) ? _cp_cat.active_line_chassis.name : _cp.flagship_chassis;

                draw_set_color(make_color_rgb(170, 195, 220));
                draw_text(_cdx + 14, _cdy + 30, "CEO: " + _cp.ceo + "  |  HQ: " + _cp.hq_location);
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_cdx + 14, _cdy + 48, "R&D Doctrine: " + _b_name);
                draw_set_color(make_color_rgb(80, 255, 140));
                draw_text(_cdx + 14, _cdy + 66, "Active Line Chassis: " + _line_suit);

                if (!is_undefined(_cp_cat) && _cp_cat.has_rare_x_spec && !is_undefined(_cp_cat.rare_x_chassis)) {
                    draw_set_color(make_color_rgb(255, 215, 60));
                    draw_text(_cdx + 14, _cdy + 84, "[PROTOTYPE X-SPEC: " + _cp_cat.rare_x_chassis.name + "]");
                } else {
                    draw_set_color(make_color_rgb(140, 160, 180));
                    draw_text(_cdx + 14, _cdy + 84, "Standard Doctrine Production (No Black-Ops Spec)");
                }'''

if target_card in content:
    content = content.replace(target_card, replacement_card)
    print("Replaced corporate card details with R&D branch and X-spec")
else:
    print("ERROR: Target for corporate card details not found!")

# Update event popup choice consequence for market_share_delta
target_ev = '''            if (variable_struct_exists(_choice, "pilot")) array_push(obj_GameManager.facilities.roster_pilots, _choice.pilot);'''
replacement_ev = '''            if (variable_struct_exists(_choice, "pilot")) array_push(obj_GameManager.facilities.roster_pilots, _choice.pilot);
            if (variable_struct_exists(_choice, "market_share_delta")) {
                obj_GameManager.pmc_market_share_pct = min(100, obj_GameManager.pmc_market_share_pct + _choice.market_share_delta);
            }'''

if target_ev in content:
    content = content.replace(target_ev, replacement_ev)
    print("Updated event popup consequence handling")
else:
    print("WARNING: target_ev not found")

with open('objects/obj_HQTerminal/Draw_64.gml', 'w') as f:
    f.write(content)

print("Saved objects/obj_HQTerminal/Draw_64.gml")
