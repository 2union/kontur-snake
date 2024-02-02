import pygame


def key_event(key: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, unicode='', key=key, mod=pygame.KMOD_NUM)


def char_event(char: str, key: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, unicode=char, key=key, mod=pygame.KMOD_NONE)


def key_up() -> None:
    up = key_event(pygame.K_UP)
    pygame.event.post(up)


def key_down() -> None:
    down = key_event(pygame.K_DOWN)
    pygame.event.post(down)


def key_left() -> None:
    left = key_event(pygame.K_LEFT)
    pygame.event.post(left)


def key_right() -> None:
    right = key_event(pygame.K_RIGHT)
    pygame.event.post(right)


def key_w() -> None:
    up = char_event('w', pygame.K_w)
    pygame.event.post(up)


def key_s() -> None:
    down = char_event('s', pygame.K_s)
    pygame.event.post(down)


def key_a() -> None:
    left = char_event('a', pygame.K_a)
    pygame.event.post(left)


def key_d() -> None:
    right = char_event('d', pygame.K_d)
    pygame.event.post(right)
