import tcod as libtcod

from entity import Entity, get_blocking_entities_at_location
from input_handlers import handle_keys
from render_functions import clear_all, render_all, RenderOrder
from map_objects.game_map import GameMap
from map_objects.tile import Tile
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from components.fighter import Fighter
from components.ai import BasicMonster
from death_functions import kill_player, kill_monster
from game_messages import MessageLog, Message

    
def main():
    screen_width = 80
    screen_height = 50
    
    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height
    
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1
    
    map_width = 80
    map_height = 43
    
    room_max_size = 30
    room_min_size = 6
    max_rooms = 30
    
    fov_algorithm = 2
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3
    max_items_per_room = 2
    
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }
    
    til = Tile(False)
   
    fighter_component = Fighter(30, defense=2, power=5)
    
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, fighter=fighter_component, render_order = RenderOrder.ACTOR)
    entities = [player]    
    
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    
    con = libtcod.console_new(screen_width, screen_height)
    panel = libtcod.console_new(screen_width, panel_height)
    
    map = GameMap(map_width, map_height)
    map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room)
    
    fov_recompute = True
    
    fov_map = initialize_fov(map)
    
    message_log = MessageLog(message_x, message_width, message_height)
    
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    
    game_state = GameStates.PLAYERS_TURN

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
            
        entities_in_render_order = sorted(entities, key = lambda x : x.render_order.value)
        
        
        
        render_all(con, panel, entities_in_render_order, player, map, fov_map, fov_recompute, message_log, screen_width, screen_height,
                   bar_width, panel_height, panel_y, mouse, colors)

        fov_recompute = False
        
        libtcod.console_flush()
        
        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        
        player_turn_results = []
        
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            if not map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True
                    
                game_state = GameStates.ENEMY_TURN
                
            else:
                message_log.add_message(Message('stuck'))
                
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        if exit:
            return True
        
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            
            if message:
                message_log.add_message(message)
                
            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)
                    
                message_log.add_message(message)
        
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities_in_render_order:
                if entity != player and entity.ai != None:
                    enemy_turn_results = entity.ai.take_turn(fov_map, player, map, entities)
                    
                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')
                        
                        if message:
                            message_log.add_message(message)
                            
                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                        message_log.add_message(message)

                        if game_state == GameStates.PLAYER_DEAD:
                            break

            game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
