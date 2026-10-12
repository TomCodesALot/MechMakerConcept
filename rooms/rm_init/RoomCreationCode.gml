/// @description rm_init Room Creation Code
// Bootstrap core manager singletons and transition to rm_hq_terminal

show_debug_message("[rm_init] ========================================");
show_debug_message("[rm_init] Initializing PMC Engine Core Architecture");
show_debug_message("[rm_init] ========================================");

// 1. Instantiate persistent obj_GameManager if not already created
if (!instance_exists(obj_GameManager)) {
    instance_create_depth(0, 0, 0, obj_GameManager);
    show_debug_message("[rm_init] Created obj_GameManager");
}

// 2. Instantiate persistent obj_FactionManager if not already created
if (!instance_exists(obj_FactionManager)) {
    instance_create_depth(0, 0, 0, obj_FactionManager);
    show_debug_message("[rm_init] Created obj_FactionManager");
}

// 3. Instantiate persistent obj_BlueprintManager if not already created
if (!instance_exists(obj_BlueprintManager)) {
    instance_create_depth(0, 0, 0, obj_BlueprintManager);
    show_debug_message("[rm_init] Created obj_BlueprintManager");
}

show_debug_message("[rm_init] Core managers initialized. Transitioning to rm_hq_terminal...");
room_goto(rm_hq_terminal);
