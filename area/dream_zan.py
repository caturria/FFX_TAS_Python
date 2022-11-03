import battle.boss
import battle.main
import battle.overdrive
import logs
import memory.main
import pathing
import rng_track
import save_sphere
import tts
import vars
import xbox

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def new_game(gamestate):
    print("Starting the game")
    print("Gamestate:", gamestate)

    last_message = 0
    # New version
    if gamestate == "none":  # New Game
        while memory.main.get_map() != 0:
            if memory.main.get_map() != 23:
                if last_message != 1:
                    last_message = 1
                    print("Attempting to get to New Game screen")
                FFXC.set_value("btn_start", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_start", 0)
                memory.main.wait_frames(1)
            elif memory.main.save_menu_open():
                if last_message != 2:
                    last_message = 2
                    print("Load Game menu is open. Backing out.")
                xbox.tap_a()
            elif memory.main.save_menu_cursor() == 1:
                if last_message != 3:
                    last_message = 3
                    print("New Game is not selected. Switching.")
                xbox.menu_up()
            else:
                if last_message != 4:
                    last_message = 4
                    print("New Game is selected. Starting game.")
                xbox.menu_b()
        memory.main.click_to_diag_progress(6)
        if game_vars.use_legacy_soundtrack():
            tts.message("Setting original soundtrack")
            memory.main.wait_frames(20)
            xbox.tap_down()
            memory.main.wait_frames(20)
            memory.main.click_to_diag_progress(8)
        else:
            memory.main.click_to_diag_progress(7)
    else:  # Load Game
        while not memory.main.save_menu_open():
            if memory.main.get_map() != 23:
                FFXC.set_value("btn_start", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_start", 0)
                memory.main.wait_frames(1)
            elif memory.main.save_menu_cursor() == 0:
                xbox.menu_down()
            else:
                xbox.menu_b()


def new_game_2():
    # New game selected. Next, select options.
    time_buffer = 15
    print("====================================")
    print("Starting in")
    print("3")
    memory.main.wait_frames(time_buffer)
    print("2")
    memory.main.wait_frames(time_buffer)
    print("1")
    memory.main.wait_frames(time_buffer)
    print("GO!!! Good fortune!")
    print("====================================")
    print("Set seed:", memory.main.rng_seed())
    xbox.menu_b()
    xbox.menu_b()


def listen_story():
    memory.main.wait_frames(10)
    vars.init_vars()
    while not memory.main.user_control():
        if memory.main.get_map() == 132:
            if memory.main.diag_progress_flag() == 1:
                game_vars.set_csr(False)
                print("Skipping intro scene, we'll watch this properly in ~8 hours")
                memory.main.await_control()
            if not game_vars.accessibility_vars()[0]:
                FFXC.set_value("btn_back", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_back", 0)
                memory.main.wait_frames(1)

    print("### CSR check:", game_vars.csr())
    checkpoint = 0
    while memory.main.get_encounter_id() != 414:  # Sinspawn Ammes
        if memory.main.user_control():
            # Events
            if checkpoint == 5:
                FFXC.set_movement(0, -1)
                while not memory.main.name_aeon_ready():
                    xbox.tap_b()
                print("Ready to name Tidus")
                FFXC.set_neutral()
                memory.main.wait_frames(1)

                # Name Tidus
                xbox.name_aeon("Tidus")
                print("Tidus name complete.")

                checkpoint += 1
            # elif checkpoint == 7 and game_vars.csr():
            #    checkpoint = 9
            elif checkpoint == 8:
                while memory.main.user_control():
                    FFXC.set_movement(1, 0)
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.await_control()
                print("Done clicking")
                checkpoint += 1
            elif checkpoint < 11 and memory.main.get_story_progress() >= 5:
                checkpoint = 11
            elif checkpoint < 21 and memory.main.get_map() == 371:
                checkpoint = 21
            elif checkpoint < 25 and memory.main.get_map() == 370:
                checkpoint = 25
            elif checkpoint == 27:  # Don't cry.
                while memory.main.user_control():
                    FFXC.set_movement(1, -1)
                FFXC.set_neutral()
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(pathing.tidus_home(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                if (
                    memory.main.get_story_progress() == 10
                    and memory.main.diag_progress_flag() == 2
                ):
                    print("Special Skip")
                    memory.main.wait_frames(130)
                    # Generate button to skip later
                    FFXC.set_value("btn_start", 1)
                    memory.main.wait_frames(1)
                    FFXC.set_value("btn_start", 0)
                    xbox.skip_dialog(10)
                else:
                    if game_vars.use_pause():
                        memory.main.wait_frames(1)
                    xbox.skip_scene(fast_mode=True)
                    xbox.skip_dialog(3)


def ammes_battle():
    print("Starting ammes")
    xbox.click_to_battle()
    memory.main.last_hit_init()
    battle.main.defend()
    # logs.write_stats("First Six Hits:")
    hits_array = []

    print("Killing Sinspawn")
    while memory.main.battle_active():
        if memory.main.turn_ready():
            battle.main.attack("none")
            last_hit = memory.main.last_hit_check_change()
            while last_hit == 9999:
                last_hit = memory.main.last_hit_check_change()
            print("Confirm - last hit:", last_hit)
            hits_array.append(last_hit)
            print(hits_array)
    print("#####################################")
    print("### Unconfirmed seed check:", memory.main.rng_seed())
    correct_seed = rng_track.hits_to_seed(hits_array=hits_array)
    logs.write_stats("Corrected RNG seed:")
    logs.write_stats(correct_seed)
    print("### Corrected RNG seed:", correct_seed)
    if correct_seed != "Err_seed_not_found":
        game_vars.set_confirmed_seed(correct_seed)
    print("Confirming RNG seed:", memory.main.rng_seed())
    print("#####################################")
    print("Done Killing Sinspawn")
    memory.main.wait_frames(6)  # Just for no overlap
    print("Clicking to battle.")
    xbox.click_to_battle()
    print("Waiting for Auron's Turn")
    print("At Overdrive")
    # Auron overdrive tutorial
    battle.overdrive.auron()


def after_ammes():
    memory.main.click_to_control()
    checkpoint = 0
    # memory.main.wait_frames(90)
    # print("#### MARK ####")
    # memory.main.ammes_fix(actor_index=0)
    # memory.main.wait_frames(90)

    while memory.main.get_map() != 49:
        if memory.main.user_control():
            start_pos = memory.main.get_coords()
            if int(start_pos[0]) in [866, 867, 868, 869, 870] and int(start_pos[1]) in [
                -138,
                -139,
                -140,
                -141,
            ]:
                print("Positioning error")
                FFXC.set_neutral()
                memory.main.wait_frames(20)
                memory.main.ammes_fix(actor_index=0)
                memory.main.wait_frames(20)
            else:
                # Map changes and events
                if checkpoint == 6:  # Save sphere
                    save_sphere.touch_and_go()
                    checkpoint += 1
                # Swim to Jecht
                elif checkpoint < 9 and memory.main.get_story_progress() >= 20:
                    checkpoint = 9
                # Towards Baaj temple
                elif checkpoint < 11 and memory.main.get_story_progress() >= 30:
                    checkpoint = 11

                # General pathing
                elif pathing.set_movement(pathing.all_starts_here(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.turn_ready():
                battle.boss.tanker()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_stored_scene(3)


def swim_to_jecht():
    print("Swimming to Jecht")

    FFXC.set_value("btn_a", 1)
    FFXC.set_movement(-1, -1)
    memory.main.wait_frames(30 * 8)
    while memory.main.user_control():
        FFXC.set_movement(-1, 1)

    FFXC.set_neutral()
    FFXC.set_value("btn_a", 0)
    print("We've now reached Jecht.")
    xbox.skip_dialog(5)

    # Next, swim to Baaj temple
    memory.main.click_to_control()
    FFXC.set_movement(1, 0)
    memory.main.wait_frames(30 * 1)
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 0.6)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 5)
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 14)
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(30 * 1.5)  # Line up with stairs

    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 3)

    while memory.main.get_map() == 48:
        pos = memory.main.get_coords()
        if pos[1] < 550:
            if pos[0] < -5:
                FFXC.set_movement(1, 1)
            elif pos[0] > 5:
                FFXC.set_movement(-1, 1)
            else:
                FFXC.set_movement(0, 1)
        else:
            if pos[1] > ((-1.00 * pos[0]) + 577.00):
                FFXC.set_movement(-1, 1)
            else:
                FFXC.set_movement(0, 1)

    FFXC.set_neutral()
    memory.main.wait_frames(30 * 0.3)