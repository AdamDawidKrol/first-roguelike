import libtcodpy as libtcod
from input_handlers import handle_keys
from entity import Entity
from render_functions import render_all, clear_all


def main():
    screen_width = 80
    screen_height = 50
    
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)
    
    map_width = 80
    map_height = 45
    
    player = Entity(player_x, player_y, '@', libtcod.white)
    npc = Entity(int(screen_width/2-5), int(screen_height/2-5), '@', libtcod.yellow)
    entities = [player, npc]

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    
    con = libtcod.console_new(screen_width, screen_height)
    
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        
        render_all(con, entities, screen_width, screen_height)
        
        libtcod.console_flush()
        
        clear_all(con, entities)

        action = handle_keys(key)
    
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        
        if move:
            dx, dy = move
            player.move(dx, dy)

        if exit:
            return True
        
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen)


if __name__ == '__main__':
    main()