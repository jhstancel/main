# main.py
from __future__ import annotations
import sys, time
import pygame as pg
import settings as S
from saveio import quick_login, Profile

# ====== MAP THESE IMPORTS to your actual function names ======
from pygame_remade import (
    # MENU scene
    init_menu, update_menu, draw_menu, handle_menu_event,
    # GAME scene
    init_game, update_game, draw_game, handle_game_event,
)
# =============================================================

def set_up_display() -> tuple[pg.Surface, pg.Surface | None]:
    screen = pg.display.set_mode((S.WINDOW_W, S.WINDOW_H), pg.RESIZABLE)
    pg.display.set_caption(S.TITLE)
    logical = pg.Surface((S.LOGICAL_W, S.LOGICAL_H), pg.SRCALPHA) if S.SCALE_TO_WINDOW else None
    return screen, logical

def blit_scaled(screen: pg.Surface, logical: pg.Surface | None):
    if logical is None:
        return
    ww, wh = screen.get_size()
    lw, lh = logical.get_size()
    screen.blit(pg.transform.smoothscale(logical, (ww, wh)), (0, 0))

def switch_scene(state: dict, name: str):
    state["scene"] = name
    scenes = state["scenes"]
    scenes[name]["init"](state)

def run():
    pg.init()
    try:
        pg.mixer.init()
    except Exception:
        pass

    clock = pg.time.Clock()
    screen, logical = set_up_display()

    # ---- global state ----
    state: dict = {
        "running": True,
        "scene": "menu",
        "dt": 0.0,
        "last_time": time.perf_counter(),
        # login/save integration
        "profile": None,       # type: Profile | None
        "login_msg": "",       # status for GUI to show
        "stats": None,         # list[str] loaded from save file
        # any other global fields your functions expect:
        # "score": 0, "level": 1, ...
    }

    # ---- register scenes ----
    state["scenes"] = {
        "menu": {
            "init":   init_menu,
            "update": update_menu,
            "draw":   draw_menu,
            "handle": handle_menu_event,
        },
        "game": {
            "init":   init_game,
            "update": update_game,
            "draw":   draw_game,
            "handle": handle_game_event,
        },
    }

    # init first scene
    state["scenes"][state["scene"]]["init"](state)

    # ---- main loop ----
    while state["running"]:
        now = time.perf_counter()
        state["dt"] = now - state["last_time"]
        state["last_time"] = now

        for event in pg.event.get():
            if event.type == pg.QUIT:
                state["running"] = False
            elif event.type == pg.VIDEORESIZE and not S.SCALE_TO_WINDOW:
                screen = pg.display.set_mode(event.size, pg.RESIZABLE)
            else:
                state["scenes"][state["scene"]]["handle"](event, state)

        state["scenes"][state["scene"]]["update"](state, state["dt"])

        target = logical if logical else screen
        target.fill(S.BLACK)
        state["scenes"][state["scene"]]["draw"](target, state)

        if logical:
            screen.fill(S.BLACK)
            blit_scaled(screen, logical)

        pg.display.flip()
        clock.tick(S.FPS)

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    run()
