# ==============================================================================
# importing
# ==============================================================================
from psychopy import visual, event, core, sound
import math
import random

# ==============================================================================
# window setup
# ==============================================================================

# use this one for fullscreen:
window = visual.Window(fullscr=True, units="norm", color="black")

#use this one for a windowed screen:
#window = visual.Window([1820,980], units="norm", color="black")

# ==============================================================================
# sound effects setup
# ==============================================================================
hit_sound    = sound.Sound('A', secs=0.1)
lose_sound_1 = sound.Sound('F', secs=0.3, octave=4)
lose_sound_2 = sound.Sound('D', secs=0.3, octave=4)
lose_sound_3 = sound.Sound('B', secs=1.2, octave=3)

# ==============================================================================
# pumpkin default variables
# ==============================================================================
pumpkin_outer_size = 0.26
pumpkin_inner_size = 0.24
pumpkin_leaf_size = 0.07
pumpkin_eye_size = 0.06
pumpkin_nose_size = 0.04
pumpkin_stem_width = 0.05
pumpkin_stem_height = 0.10
pumpkin_mouth_width = 0.13
pumpkin_mouth_height = 0.03

pumpkin_x_position = 0.0
pumpkin_y_position = 0.0

# ==============================================================================
# skin assets
# ==============================================================================
skins = {
    "body": {
        "orange": {"outer_color": "#ff7b00", "inner_color": "#ff9b33"},
        "white":  {"outer_color": "#ffffff", "inner_color": "#dddddd"},
        "black":  {"outer_color": "#222222", "inner_color": "#555555"},
        "purple": {"outer_color": "#800080", "inner_color": "#b19cd9"},
        "green":  {"outer_color": "#2a7b1b", "inner_color": "#58a65c"}
    },
    "eyes": {
        "triangle": {"edges":  3, "color": "black"},
        "circle":   {"edges": 20, "color": "black"},
        "yellow":   {"edges":  5, "color": "yellow"},
        "blue":     {"edges":  4, "color": "blue"},
        "red":      {"edges":  6, "color": "red"}
    },
    "mouth": {
        "black":  {"width": pumpkin_mouth_width,"height": pumpkin_mouth_height,"color": "black"},
        "green":  {"width": pumpkin_mouth_width,"height": pumpkin_mouth_height,"color": "green"},
        "red":    {"width": pumpkin_mouth_width,"height": pumpkin_mouth_height,"color": "red"},
        "blue":   {"width": pumpkin_mouth_width,"height": pumpkin_mouth_height,"color": "blue"},
        "orange": {"width": pumpkin_mouth_width,"height": pumpkin_mouth_height,"color": "orange"}
    },
    "stem": {
        "green":  {"stem_color":"#2a7b1b", "leaf_color":"#2a7b1b"},
        "brown":  {"stem_color":"#8b4513", "leaf_color":"#8b4513"},
        "yellow": {"stem_color":"#ffff00", "leaf_color":"#ffff00"},
        "red":    {"stem_color":"#ff0000", "leaf_color":"#ff0000"},
        "purple": {"stem_color":"#800080", "leaf_color":"#800080"}
    }
}

# currently equipped skin
current_skin = {"body":"orange","eyes":"triangle","mouth":"black","stem":"green"}


# ==============================================================================
# create pumpkin
# ==============================================================================
def create_pumpkin(x, y, skin=None):
    if skin is None: 
        skin = current_skin

    body_skin  = skins["body"][skin["body"]]
    eye_skin   = skins["eyes"][skin["eyes"]]
    mouth_skin = skins["mouth"][skin["mouth"]]
    stem_skin  = skins["stem"][skin["stem"]]

    outer_shell = visual.Polygon(window, edges=10, fillColor=body_skin["outer_color"], lineColor=body_skin["outer_color"], size=pumpkin_outer_size, pos=(x, y))
    inner_shell = visual.Polygon(window, edges=10, fillColor=body_skin["inner_color"], lineColor=body_skin["inner_color"], size=pumpkin_inner_size, pos=(x, y))
    leaf        = visual.Polygon(window, edges= 3, fillColor=stem_skin["leaf_color"],  lineColor=stem_skin["leaf_color"],  size=pumpkin_leaf_size,  pos=(x + 0.035, y + 0.18), ori=45)
    nose        = visual.Polygon(window, edges= 3, fillColor="black",                  lineColor="black",                  size=pumpkin_nose_size,  pos=(x, y - 0.025), ori=180)
    
    left_eye    = visual.Polygon(window, edges=eye_skin["edges"], fillColor=eye_skin["color"], lineColor=eye_skin["color"], size=pumpkin_eye_size,  pos=(x - 0.06, y + 0.035), ori=180)
    right_eye   = visual.Polygon(window, edges=eye_skin["edges"], fillColor=eye_skin["color"], lineColor=eye_skin["color"], size=pumpkin_eye_size,  pos=(x + 0.06, y + 0.035), ori=180)
    
    mouth = visual.Rect(window, width=mouth_skin["width"], height=mouth_skin["height"], fillColor=mouth_skin["color"],     lineColor=mouth_skin["color"],     pos=(x, y - 0.08))
    stem  = visual.Rect(window, width=pumpkin_stem_width,  height=pumpkin_stem_height,  fillColor=stem_skin["stem_color"], lineColor=stem_skin["stem_color"], pos=(x, y + 0.14))

    return {
        "outer_shell": outer_shell,
        "inner_shell": inner_shell,
        "leaf": leaf,
        "left_eye": left_eye,
        "right_eye": right_eye,
        "nose": nose,
        "mouth": mouth,
        "stem": stem,
        "scale": 1.0,
        "pumpkin_x_position": x,
        "pumpkin_y_position": y
    }


# ==============================================================================
# set pumpkin scale
# ==============================================================================
def set_pumpkin_scale(pumpkin, scale):
    pumpkin["outer_shell"]  .setSize(pumpkin_outer_size   * scale)
    pumpkin["inner_shell"]  .setSize(pumpkin_inner_size   * scale)
    pumpkin["leaf"]         .setSize(pumpkin_leaf_size    * scale)
    pumpkin["left_eye"]     .setSize(pumpkin_eye_size     * scale)
    pumpkin["right_eye"]    .setSize(pumpkin_eye_size     * scale)
    pumpkin["nose"]         .setSize(pumpkin_nose_size    * scale)
    pumpkin["mouth"]        .setSize((pumpkin_mouth_width * scale, pumpkin_mouth_height * scale))
    pumpkin["stem"]         .setSize((pumpkin_stem_width  * scale, pumpkin_stem_height  * scale))

# ==============================================================================
# set pumpkin rotation
# ==============================================================================
def set_pumpkin_rotation(pumpkin, rotation):
    pumpkin["outer_shell"]  .setOri(rotation)
    pumpkin["inner_shell"]  .setOri(rotation)
    pumpkin["leaf"]         .setOri(rotation+ 45)
    pumpkin["left_eye"]     .setOri(rotation+180)
    pumpkin["right_eye"]    .setOri(rotation+180)
    pumpkin["nose"]         .setOri(rotation+180)
    pumpkin["mouth"]        .setOri(rotation)
    pumpkin["stem"]         .setOri(rotation)


# ==============================================================================
# update pumpkin position
# ==============================================================================
def update_pumpkin_position(pumpkin, new_x, new_y):
    scale = pumpkin.get("scale", 1.0)
    
    pumpkin["pumpkin_x_position"] = new_x
    pumpkin["pumpkin_y_position"] = new_y
    
    pumpkin["outer_shell"]  .pos = (new_x + 0.000 * scale, new_y + 0.000 * scale)
    pumpkin["inner_shell"]  .pos = (new_x + 0.000 * scale, new_y + 0.000 * scale)
    pumpkin["leaf"]         .pos = (new_x + 0.035 * scale, new_y + 0.180 * scale)
    pumpkin["left_eye"]     .pos = (new_x - 0.060 * scale, new_y + 0.035 * scale)
    pumpkin["right_eye"]    .pos = (new_x + 0.060 * scale, new_y + 0.035 * scale)
    pumpkin["nose"]         .pos = (new_x + 0.000 * scale, new_y - 0.025 * scale)
    pumpkin["mouth"]        .pos = (new_x + 0.000 * scale, new_y - 0.080 * scale)
    pumpkin["stem"]         .pos = (new_x + 0.000 * scale, new_y + 0.140 * scale)

# ==============================================================================
# draw all pumpkin parts
# ==============================================================================
def draw_pumpkin(pumpkin):
    pumpkin["outer_shell"]  .draw()
    pumpkin["inner_shell"]  .draw()
    pumpkin["leaf"]         .draw()
    pumpkin["left_eye"]     .draw()
    pumpkin["right_eye"]    .draw()
    pumpkin["nose"]         .draw()
    pumpkin["mouth"]        .draw()
    pumpkin["stem"]         .draw()

# ==============================================================================
# reset all pumpkin parts
# ==============================================================================
def reset_pumpkin_to_defaults(pumpkin):
    
    set_pumpkin_scale(pumpkin, 1.0)
    update_pumpkin_position(pumpkin, 0.0, 0.0)
    
    pumpkin["outer_shell"]  .setOri(0)
    pumpkin["inner_shell"]  .setOri(0)
    pumpkin["leaf"]         .setOri(45)
    pumpkin["left_eye"]     .setOri(180)
    pumpkin["right_eye"]    .setOri(180)
    pumpkin["nose"]         .setOri(180)
    pumpkin["mouth"]        .setOri(0)
    pumpkin["stem"]         .setOri(0)

# ==============================================================================
# start menu
# ==============================================================================
def start_menu():
    # menu options
    menu_options = ["Play PONG  ", "Listen to Music  ", "Squash Squash  ", "Skin Store  "] # 2 spaces as a suffix needed because I add 2 characters as a prefix later on
    selected_option = 0
    
    # pumpkin menu bounce parameters
    bounce_speed = 1 / 20.0
    bounce_frame = 0 # needed for bouncing pumpkins
    
    # create menu text
    title        = visual.TextStim(window, text="Happy Halloween!", pos=(0, 0.55), height=0.12, color='orange', bold=True)
    instructions = visual.TextStim(window, text="Use ↑/↓ to navigate | SPACE to select | ESC to quit", pos=(0, -0.8), height=0.05, color='gray')
    
    # create the menu pumpkins
    menu_pumpkin_left  = create_pumpkin(-0.6, 0)
    menu_pumpkin_right = create_pumpkin(+0.6, 0)
    set_pumpkin_scale(menu_pumpkin_left,  1.15)
    set_pumpkin_scale(menu_pumpkin_right, 1.15)
    
    # main menu loop
    while True:
        # bouncing the menu pumpkins
        bounce_frame += 1
        y_offset = 0.08 * math.sin(bounce_frame * bounce_speed)
        update_pumpkin_position(menu_pumpkin_left,  -0.6, +y_offset)
        update_pumpkin_position(menu_pumpkin_right, +0.6, -y_offset)
        draw_pumpkin(menu_pumpkin_left)
        draw_pumpkin(menu_pumpkin_right)
        
        # drawing the normal texts
        title.draw()
        instructions.draw()
        
        # menu selection
        menu_option_spacing = 0.12
        for index, option in enumerate(menu_options):
            if index == selected_option:
                prefix = "> "
            else:
                prefix = "  "
            menu_option = visual.TextStim(window, text=f"{prefix}{option}", pos=(0, 0.15 - index*menu_option_spacing), height=0.07, color='white', italic=True) # index*0.12 --> controls y_space between menu options
            menu_option.draw()
        
        # get key inputs
        keys_pressed = event.getKeys()
        if 'up' in keys_pressed: 
            selected_option = (selected_option - 1) % len(menu_options)
        if 'down' in keys_pressed: 
            selected_option = (selected_option + 1) % len(menu_options)
        if 'space' in keys_pressed or 'return' in keys_pressed: 
            return selected_option
        if 'escape' in keys_pressed:
            window.close()
            core.quit()
        
        # update the window at 60 FPS
        window.flip()
        core.wait(1/60.0)

# ==============================================================================
# skin store
# ==============================================================================
def skin_store(pong_high_score, squash_high_score):
    event.clearEvents()

    # order of pumpkin parts to edit
    parts_order = ["body","eyes","mouth","stem"]
    selected_part_index = 0

    part_skins = {
        "body":  ["orange",  "white", "black", "purple","green"],
        "eyes":  ["triangle","circle","yellow","blue",  "red"],
        "mouth": ["black",   "green", "red",   "blue",  "orange"],
        "stem":  ["green",   "brown", "yellow","red",   "purple"]
    }

    # unlock scores for example
    skin_unlock_scores = {
        "body":  {"orange":0,  "white":3, "black":5, "purple":8,"green":12},
        "eyes":  {"triangle":0,"circle":3,"yellow":7,"blue":10, "red":15},
        "mouth": {"black":0,   "green":5, "red":10,  "blue":12, "orange":18},
        "stem":  {"green":0,   "brown":1, "yellow":5,"red":8,   "purple":12}
    }
    
    # scroll index for current part
    scroll_index = 0
    visible_count = 5

    # UI texts
    title = visual.TextStim(window, text="Pumpkin Skin Store", pos=(0, 0.55), height=0.10, color="orange", bold=True)
    instructions = visual.TextStim(window, text="Use ↑/↓ to switch part | ←/→ to scroll | SPACE to equip | ESC to exit", pos=(0, -0.8), height=0.05, color="gray")
    part_text = visual.TextStim(window, text="", pos=(0, -0.65), height=0.08, color="white", bold=True)
    unlock_text_object = visual.TextStim(window, height=0.03, bold=True)
    
    while True:
        title.draw()
        instructions.draw()
        
        # current part
        selected_part = parts_order[selected_part_index]
        skins = part_skins[selected_part]
        
        # determine visible range for carousel
        half_visible = visible_count // 2
        total_skins = len(skins)
        spacing = 0.35
        
        # draw carousel pumpkins
        for offset in range(-half_visible, half_visible + 1):
            index = scroll_index + offset
            if 0 <= index < total_skins:
                x = offset * spacing
                y = 0.0
                skin_name = skins[index]
                skin_pumpkin = create_pumpkin(x, y, skin={**current_skin, selected_part: skin_name})
                draw_pumpkin(skin_pumpkin)

                # display unlock scores clearly
                unlock_score = skin_unlock_scores[selected_part][skin_name]
                unlocked = unlock_score <= pong_high_score
                if unlocked:
                    unlock_text_object.text = f"Unlocked!"
                    unlock_text_object.color = "white"
                else:
                    unlock_text_object.text = f"Pong high score needed: {unlock_score}"
                    unlock_text_object.color = "red"
                    
                unlock_text_object.pos = (x, y - 0.15)
                unlock_text_object.draw()

        # display current part
        part_text.text = f"Editing: {selected_part.upper()}  |  Selected Skin: {skins[scroll_index]}"
        part_text.draw()
        
        # handle input
        keys = event.getKeys()
        if 'up' in keys:
            selected_part_index = (selected_part_index - 1) % len(parts_order)
            scroll_index = 0
        if 'down' in keys:
            selected_part_index = (selected_part_index + 1) % len(parts_order)
            scroll_index = 0
        if 'left' in keys:
            if scroll_index > 0:
                scroll_index -= 1
        if 'right' in keys:
            if scroll_index < len(skins) - 1:
                scroll_index += 1
        if 'space' in keys or 'return' in keys:
            # equip only if unlocked
            unlock_score = skin_unlock_scores[selected_part][skins[scroll_index]]
            if unlock_score <= pong_high_score:
                current_skin[selected_part] = skins[scroll_index]
                hit_sound.play()
                core.wait(0.10+0.10)
                hit_sound.play()
            else:
                lose_sound_1.play()
                core.wait(0.30+0.10)
                lose_sound_2.play()
                core.wait(0.30+0.10)
                lose_sound_3.play()
        if 'escape' in keys:
            return
        
        window.flip()
        core.wait(1/60.0)


# ==============================================================================
# pong difficulty menu
# ==============================================================================
def pong_difficulty_menu():
    options = ["Easy  ", "Medium  ", "Hard  "] # 2 spaces as  suffix needed because I add 2 characters as a prefix later on
    speed = [0.010, 0.014, 0.020]
    selected_option = 1 # defaults to medium difficulty
    title = visual.TextStim(window, text="Select your difficulty:", pos=(0, 0.55), height=0.12, color='orange', bold = True)
    instructions = visual.TextStim(window, text="Use ↑/↓ to navigate | SPACE to select | ESC to quit", pos=(0, -0.8), height=0.05, color='gray')

    while True:
        # drawing the normal texts
        title.draw()
        instructions.draw()
        
        # menu selection
        menu_option_spacing = 0.12
        for index, option in enumerate(options):
            if index == selected_option:
                prefix = "> "
            else:
                prefix = "  "
            menu_option = visual.TextStim(window, text=f"{prefix}{option}", pos=(0, 0.15 - index*menu_option_spacing), height=0.07, color='white', italic=True)
            menu_option.draw()

        # get key inputs
        keys_pressed = event.getKeys()
        if 'up' in keys_pressed:
            selected_option = (selected_option - 1) % len(options)
        if 'down' in keys_pressed:
            selected_option = (selected_option + 1) % len(options)
        if 'space' in keys_pressed or 'return' in keys_pressed:
            return speed[selected_option]
        if 'escape' in keys_pressed:
            return None
        
        # update the window at 60 FPS
        window.flip()
        core.wait(1/60.0)

# ==============================================================================
# music score
# ==============================================================================
def spooky_music(tempo):
    # play a sequence of spooky sounds
    la3 = sound.Sound('A', octave=4, secs=tempo)
    la3_point = sound.Sound('A', octave=4, secs=tempo*1.5)
    la3_long = sound.Sound('A', octave=4, secs=tempo*2)
    la3_loong = sound.Sound('A', octave=4, secs=tempo*4)
    si3_point = sound.Sound('B', octave=4, secs=tempo*1.5)
    do4 = sound.Sound('C', octave=5, secs=tempo)
    do4_half = sound.Sound('C', octave=5, secs=tempo/2)
    re4 = sound.Sound('D', octave=5, secs=tempo)
    mi4 = sound.Sound('E', octave=5, secs=tempo)
    fa4 = sound.Sound('F', octave=5, secs=tempo)
    fa4_half = sound.Sound('F', octave=5, secs=tempo/2)
    fa4_point = sound.Sound('F', octave=5, secs=tempo*1.5)

    sequence = [
        (fa4, tempo), (fa4, tempo), (mi4, tempo), (mi4, tempo),
        (la3, tempo), (do4_half, tempo/2), (la3_point, tempo*1.5),
        (la3, tempo),
        (fa4_half, tempo/2), (fa4_point, tempo*1.5), (mi4, tempo), (mi4, tempo),
        (la3, tempo), (0, 3*tempo),
        (fa4, tempo), (fa4, tempo), (mi4, tempo), (mi4, tempo),
        (la3, tempo), (do4, tempo), (la3_long, tempo*2),
        (do4, tempo), (re4, tempo), (si3_point, tempo*1.5), (do4_half, tempo/2),
        (la3_loong, tempo*4)
    ]

    for note, wait_time in sequence:
        if note != 0:
            note.play()
        core.wait(wait_time + 0.1)

# ==============================================================================
# music screen
# ==============================================================================
def music_screen():
    # make the screen empty
    window.clearBuffer()
    
    # create grid variables
    grid_rows = 4
    grid_columns = 5
    cell_spacing = 0.35
    
    start_x = -( (grid_columns - 1) * cell_spacing ) / 2
    start_y = +( (grid_rows    - 1) * cell_spacing ) / 2
    
    # create and update the music pumpkin
    music_pumpkins = []
    for row in range(grid_rows):
        for column in range(grid_columns):
            x = start_x + column * cell_spacing
            y = start_y - row    * cell_spacing
            pumpkin = create_pumpkin(x, y)
            update_pumpkin_position(pumpkin, x, y)
            music_pumpkins.append(pumpkin)
            
    # draw the music pumpkins
    for index in range(len(music_pumpkins)):
        draw_pumpkin(music_pumpkins[index])
    window.flip()
    
    # play the music
    spooky_music(0.3)
    
    # clear the key inputs so it doesnt quit out of the game when music is done
    event.clearEvents()
    # wait a bit so you can process the greatness that just happened
    core.wait(0.50)
    
    # exit to main menu
    return None

# ==============================================================================
# pong game
# ==============================================================================
def run_pong(ball_speed_x, pong_high_score):
    # create text
    pong_score_text      = visual.TextStim(window, pos=(0, 0.90), height=0.08, color='white')
    pong_high_score_text = visual.TextStim(window, pos=(0, 0.82), height=0.05, color='white')

    # pong game boolean
    replay_pong_game = True
    
    # pong pumpkin
    pong_pumpkin = create_pumpkin(0.0, 0.0)
    
    # pong ball speed
    ball_speed_y = ball_speed_x / 2.5

    # create the pong paddle
    paddle_height = 0.25
    paddle_width  = 0.03
    paddle_x_position = -0.95
    paddle_y_position = +0.00
    paddle_rectangle = visual.Rect(window, width=paddle_width, height=paddle_height, fillColor='white', lineColor='white')
    
    # pong game loop
    while replay_pong_game:
        # set start point for pong ball
        ball_x_position = 0.0
        ball_y_position = random.uniform(-0.80,0.80) # random starting position so there is no fixed pattern in the game
        
        # reset pumpkin & paddle to start position
        update_pumpkin_position(pong_pumpkin, ball_x_position, ball_y_position)
        paddle_y_position = 0
        
        # start with a score of 0
        pong_score = 0
        
        # pong game boolean
        pong_game_running = True
        
        # pong game loop
        while pong_game_running:
            keys_pressed = event.getKeys()
            if 'up' in keys_pressed: 
                paddle_y_position += 0.08
            if 'down' in keys_pressed: 
                paddle_y_position -= 0.08
            if 'escape' in keys_pressed: 
                # clear the window
                window.clearBuffer()
                
                # set the pong high score
                if pong_score > pong_high_score:
                    pong_high_score = pong_score
                    
                # game over text
                game_over_text = visual.TextStim(window, text=f"Game Over!\n\nScore: {pong_score}\nHigh Score: {pong_high_score}\n\nPress R to replay or SPACE to return to menu", pos=(0, 0), height=0.07, color='white')
                game_over_text.draw()
                window.flip()
                
                # game over screen
                while True:
                    keys_pressed = event.getKeys(['escape', 'r', 'space'])
                    if 'r' in keys_pressed:
                        ball_speed_x = abs(ball_speed_x) # makes sure the ball direction gets reset
                        pong_game_running = False # restarts the game
                        window.clearBuffer() # clear the window
                        break
                    if 'space' in keys_pressed or 'escape' in keys_pressed or 'return' in keys_pressed: 
                        return pong_high_score

            # move ball
            ball_x_position += ball_speed_x
            ball_y_position += ball_speed_y
            update_pumpkin_position(pong_pumpkin, ball_x_position, ball_y_position)

            # bounce top/bottom & right wall
            ball_radius = 0.5 * pumpkin_outer_size * pong_pumpkin.get("scale", 1.0)
            if ball_y_position + ball_radius > +1.0:
                ball_speed_y *= -1
                hit_sound.play()
            if ball_y_position - ball_radius < -1.0:
                ball_speed_y *= -1
                hit_sound.play()
            if ball_x_position + ball_radius >= 1.0:
                ball_speed_x *= -1
                hit_sound.play()

            # paddle collision
            paddle_top    = paddle_y_position + paddle_height / 2
            paddle_bottom = paddle_y_position - paddle_height / 2
            paddle_right  = paddle_x_position + paddle_width  / 2
            if (ball_x_position - ball_radius <= paddle_right and paddle_bottom < ball_y_position < paddle_top):
                ball_speed_x *= -1
                pong_score += 1
                hit_sound.play()

            # lose condition
            if ball_x_position - ball_radius <= -1.0:
                lose_sound_1.play()
                core.wait(0.45)
                lose_sound_2.play()
                core.wait(0.45)
                lose_sound_3.play()
                game_over_animation()
                
                # set the pong high score
                if pong_score > pong_high_score:
                    pong_high_score = pong_score
                
                # clear the window
                window.clearBuffer()
                
                # game over text
                game_over_text = visual.TextStim(window, text=f"Game Over!\n\nScore: {pong_score}\nHigh Score: {pong_high_score}\n\nPress R to replay or SPACE to return to menu", pos=(0, 0), height=0.07, color='white')
                game_over_text.draw()
                window.flip()
                
                # game over screen
                while True:
                    keys_pressed = event.getKeys(['escape', 'r', 'space'])
                    if 'r' in keys_pressed:
                        ball_speed_x = abs(ball_speed_x) # makes sure the ball direction gets reset
                        pong_game_running = False # restarts the game
                        window.clearBuffer() # clear the window
                        break
                    if 'space' in keys_pressed or 'escape' in keys_pressed or 'return' in keys_pressed: 
                        return pong_high_score

            # draw everything
            paddle_rectangle.pos = (paddle_x_position, paddle_y_position)
            paddle_rectangle.draw()
            
            pong_score_text.text = f"Score: {pong_score}"
            pong_high_score_text.text = f"High Score: {pong_high_score}"
            pong_score_text.draw()
            pong_high_score_text.draw()
            
            draw_pumpkin(pong_pumpkin)
            
            window.flip()
            core.wait(1/240)

# ==============================================================================
# game over animation
# ==============================================================================
def game_over_animation():
    # clear the screen
    window.clearBuffer()
    
    # create all the visual objects
    fade_rectangle = visual.Rect(window, width=2, height=2, fillColor='black', lineColor='black', opacity=0.0)
    game_over_pumpkin = create_pumpkin(0.0, 0.0)
    game_over_pumpkin_y = 0.00
    
    # number of steps
    steps = 80
    
    # get the starting scale
    scale = game_over_pumpkin.get("scale")
    
    # rumble settings
    rumble_degrees = 13
    rumble_speed = steps / 8
    
    for i in range(steps):
        # set the scale
        scale *= 1.04
        game_over_pumpkin["scale"] = scale # update dictionary so positions are correct
        set_pumpkin_scale(game_over_pumpkin, scale)
        
        # reset pumpkin positions based on the new scale
        game_over_pumpkin_y += 0.00
        update_pumpkin_position(game_over_pumpkin, 0.0, game_over_pumpkin_y)
        
        # apply rotation to all pumpkin parts
        rotation = rumble_degrees * math.sin( (2 * math.pi) * i / rumble_speed )
        set_pumpkin_rotation(game_over_pumpkin, rotation)
        
        # fade in black rectangle
        fade_rectangle.opacity = i / steps
        
        # draw everything
        draw_pumpkin(game_over_pumpkin)
        fade_rectangle.draw()
        
        # update window at 60 FPS
        window.flip()
        core.wait(1/60.0)

# ==============================================================================
# squash difficulty menu
# ==============================================================================
def squash_difficulty_menu():
    options = ["Easy  ", "Medium  ", "Hard  "] # 2 spaces as  suffix needed because I add 2 characters as a prefix later on
    
    difficulty = [0, 1, 2]
    
    selected_option = 1 # defaults to medium difficulty
    
    title = visual.TextStim(window, text="Select your difficulty:", pos=(0, 0.55), height=0.12, color='orange', bold = True)
    instructions = visual.TextStim(window, text="Use ↑/↓ to navigate | SPACE to select | ESC to quit", pos=(0, -0.8), height=0.05, color='gray')

    while True:
        # drawing the normal texts
        title.draw()
        instructions.draw()
        
        # menu selection
        menu_option_spacing = 0.12
        for index, option in enumerate(options):
            if index == selected_option:
                prefix = "> "
            else:
                prefix = "  "
            menu_option = visual.TextStim(window, text=f"{prefix}{option}", pos=(0, 0.15 - index*menu_option_spacing), height=0.07, color='white', italic=True)
            menu_option.draw()

        # get key inputs
        keys_pressed = event.getKeys()
        if 'up' in keys_pressed:
            selected_option = (selected_option - 1) % len(options)
        if 'down' in keys_pressed:
            selected_option = (selected_option + 1) % len(options)
        if 'space' in keys_pressed or 'return' in keys_pressed:
            return difficulty[selected_option]
        if 'escape' in keys_pressed:
            return None # exits the difficulty selection --> returns to the start
        
        # update the window at 60 FPS
        window.flip()
        core.wait(1/60.0)

# ==============================================================================
# squash time menu
# ==============================================================================
def squash_game_time_menu():
    options = ["10s  ", "20s  ", "30s  "] # 2 spaces as  suffix needed because I add 2 characters as a prefix later on
    
    total_game_time = [10, 20, 30]
    
    selected_option = 1 # defaults to medium difficulty
    
    title = visual.TextStim(window, text="Select your difficulty:", pos=(0, 0.55), height=0.12, color='orange', bold = True)
    instructions = visual.TextStim(window, text="Use ↑/↓ to navigate | SPACE to select | ESC to quit", pos=(0, -0.8), height=0.05, color='gray')

    while True:
        # drawing the normal texts
        title.draw()
        instructions.draw()
        
        # menu selection
        menu_option_spacing = 0.12
        for index, option in enumerate(options):
            if index == selected_option:
                prefix = "> "
            else:
                prefix = "  "
            menu_option = visual.TextStim(window, text=f"{prefix}{option}", pos=(0, 0.15 - index*menu_option_spacing), height=0.07, color='white', italic=True)
            menu_option.draw()

        # get key inputs
        keys_pressed = event.getKeys()
        if 'up' in keys_pressed:
            selected_option = (selected_option - 1) % len(options)
        if 'down' in keys_pressed:
            selected_option = (selected_option + 1) % len(options)
        if 'space' in keys_pressed or 'return' in keys_pressed:
            return total_game_time[selected_option]
        if 'escape' in keys_pressed:
            return None # exits the difficulty selection --> returns to the start
        
        # update the window at 60 FPS
        window.flip()
        core.wait(1/60.0)


# ==============================================================================
# squash squash
# ==============================================================================
def squash_squash_game(squash_difficulty, total_game_time, squash_high_score):
    # define variables
    squash_score = 0
    if squash_difficulty == 0:
        grid_rows          = 3
        grid_columns       = 3
        cell_spacing       = 0.40
        pumpkin_spawn_time = 1.50
    elif squash_difficulty == 1:
        grid_rows          = 4
        grid_columns       = 4
        cell_spacing       = 0.35
        pumpkin_spawn_time = 1.00
    elif squash_difficulty == 2:
        grid_rows          = 4
        grid_columns       = 5
        cell_spacing       = 0.30
        pumpkin_spawn_time = 0.60
        
    squash_score_text      = visual.TextStim(window, pos=(0, 0.90), height=0.08, color='white')
    squash_high_score_text = visual.TextStim(window, pos=(0, 0.82), height=0.05, color='white')
    time_display           = visual.TextStim(window, pos=(-0.30, 0.86), height=0.08, color='orange')

    # calculate grid start position
    start_x = -( (grid_columns - 1) * cell_spacing ) / 2
    start_y = +( (grid_rows    - 1) * cell_spacing ) / 2

    # create pumpkins for each cell
    grid_pumpkins = []
    for row in range(grid_rows):
        for column in range(grid_columns):
            x = start_x + column * cell_spacing
            y = start_y - row    * cell_spacing
            pumpkin = create_pumpkin(x, y)
            update_pumpkin_position(pumpkin, x, y)
            grid_pumpkins.append(pumpkin)

    # create visible grid lines
    grid_lines  = []
    grid_width  = (grid_columns - 1) * cell_spacing
    grid_height = (grid_rows -    1) * cell_spacing

    # vertical lines
    for i in range(grid_columns + 1):
        x = start_x - (cell_spacing / 2) + i * cell_spacing
        line = visual.Line(window, start=(x, start_y + (cell_spacing / 2)), end=(x, start_y - grid_height - (cell_spacing / 2)), lineColor='gray', lineWidth=2)
        grid_lines.append(line)

    # horizontal lines
    for j in range(grid_rows + 1):
        y = start_y + (cell_spacing / 2) - j * cell_spacing
        line = visual.Line(window, start=(start_x - (cell_spacing / 2), y), end=(start_x + grid_width + (cell_spacing / 2), y), lineColor='gray', lineWidth=2)
        grid_lines.append(line)
    
    replay_squash_game = True
    while replay_squash_game:
        # game timing setup
        game_clock = core.Clock()
        active_pumpkin = None
        next_spawn_time = 0
        mouse = event.Mouse()

        # reset score each round
        squash_score = 0

        # main game loop
        while game_clock.getTime() < total_game_time:
            current_time = game_clock.getTime()
            time_left = max(0, int(total_game_time - current_time))

            # choose a pumpkin to activate
            if active_pumpkin is None or current_time >= next_spawn_time:
                active_pumpkin = random.choice(grid_pumpkins)
                next_spawn_time = current_time + pumpkin_spawn_time

            # clear and draw grid
            window.clearBuffer()
            for line in grid_lines:
                line.draw()

            # draw only the active pumpkin
            for pumpkin in grid_pumpkins:
                if pumpkin == active_pumpkin:
                    draw_pumpkin(pumpkin)

            # draw text
            squash_score_text       .text = f"Score: {squash_score}"
            squash_high_score_text  .text = f"High Score: {squash_high_score}"
            time_display            .text = f"Time Left: {time_left}s"
            
            squash_score_text.draw()
            squash_high_score_text.draw()
            time_display.draw()

            window.flip()

            # handle mouse click
            if mouse.getPressed()[0]:
                if active_pumpkin is not None:
                    mouse_x, mouse_y = mouse.getPos()
                    pumpkin_x = active_pumpkin["pumpkin_x_position"]
                    pumpkin_y = active_pumpkin["pumpkin_y_position"]
                    if abs(mouse_x - pumpkin_x) < 0.1 and abs(mouse_y - pumpkin_y) < 0.1:
                        squash_score += 1
                        active_pumpkin = None
                        hit_sound.play()
                        core.wait(0.15)  # debounce time

            # exit with escape key
            keys_pressed = event.getKeys()
            if 'escape' in keys_pressed:
                break

            core.wait(1/60.0)

        # end of timer
        if squash_score > squash_high_score:
            squash_high_score = squash_score

        # clear the window
        window.clearBuffer()
        
        # game over text
        game_over_text = visual.TextStim(window, text=f"Time's up!\n\nScore: {squash_score}\nHigh Score: {squash_high_score}\n\nPress R to replay or SPACE to return to menu", pos=(0, 0), height=0.07, color='white')
        game_over_text.draw()
        window.flip()
        
        # game over screen (rewritten like Pong)
        while True:
            keys_pressed = event.getKeys(['up', 'down', 'escape', 'r', 'space'])
            if 'r' in keys_pressed:
                replay_squash_game = True  # restarts the game
                window.clearBuffer()       # clear the window
                break
            if 'space' in keys_pressed or 'escape' in keys_pressed or 'return' in keys_pressed: 
                return squash_high_score

            core.wait(1/60.0)

# ==============================================================================
# main game loop
# ==============================================================================
pong_high_score = 0
squash_high_score = 0

while True:
    menu_choice = start_menu() # returns 0 (pong) or 1 (music) or 2 (squash)
    
    # pong
    if menu_choice == 0:
        pong_difficulty = pong_difficulty_menu()
        if pong_difficulty != None:
            pong_high_score = run_pong(pong_difficulty, pong_high_score)

    # music
    elif menu_choice == 1:
        music_screen()

    # squash
    elif menu_choice == 2:
        squash_difficulty = squash_difficulty_menu()
        if squash_difficulty != None:
            total_game_time = squash_game_time_menu()
            if total_game_time != None:
                squash_high_score = squash_squash_game(squash_difficulty, total_game_time, squash_high_score)
    
    # skin store
    elif menu_choice == 3:
        skin_store(pong_high_score,squash_high_score)
