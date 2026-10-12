/// @description obj_GameManager Step Event
// Turn-based game architecture: no real-time clock advancing!
// Global keyboard shortcuts (SPACE to end turn when in command deck)

if (keyboard_check_pressed(vk_space)) {
    if (room == rm_hq_terminal && instance_exists(obj_HQTerminal)) {
        if (obj_HQTerminal.active_tutorial_modal == "" && !obj_HQTerminal.show_turn_briefing_modal && is_undefined(active_event_popup)) {
            end_turn();
        }
    }
}
