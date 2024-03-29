import tcod as libtcod


def handle_keys(key):
    key_char = chr(key.c)

    if key.vk == libtcod.KEY_UP or key_char == '8':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == '2':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == '4':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == '6':
        return {'move': (1, 0)}
    elif key_char == 'y' or key_char == '7':
        return {'move': (-1, -1)}
    elif key_char == 'u' or key_char == '9':
        return {'move': (1, -1)}
    elif key_char == 'b' or key_char == '1':
        return {'move': (-1, 1)}
    elif key_char == 'n' or key_char == '3':
        return {'move': (1, 1)}

    if key.vk == libtcod.KEY_ENTER:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}