import streamlit as st
import random
import time


# ==========================================================
# CONFIGURATION
# ==========================================================

WIDTH =  fifty = 50
HEIGHT = 28

FRAME_DELAY = 0.08


# ==========================================================
# STREAMLIT SETTINGS
# ==========================================================

st.set_page_config(
    page_title="ASCII Space Invaders",
    page_icon="👾",
    layout="centered"
)


# ==========================================================
# GAME OBJECTS
# ==========================================================


class Player:

    def __init__(self):

        self.x = WIDTH // 2
        self.y = HEIGHT - 3

        self.symbol = "^"

        self.lives = 3

        self.cooldown = 0



    def move_left(self):

        self.x = max(
            1,
            self.x - 2
        )



    def move_right(self):

        self.x = min(
            WIDTH - 2,
            self.x + 2
        )



class Bullet:

    def __init__(self, x, y, direction):

        self.x = x
        self.y = y

        self.direction = direction

        self.active = True


    def update(self):

        self.y += self.direction


        if self.y <= 0 or self.y >= HEIGHT:

            self.active = False



# ==========================================================
# STAR FIELD
# ==========================================================


class StarField:

    def __init__(self):

        self.stars = []

        for _ in range(70):

            self.stars.append(
                [
                    random.randint(1, WIDTH-2),
                    random.randint(1, HEIGHT-2)
                ]
            )


    def update(self):

        for star in self.stars:

            star[1] += 1


            if star[1] >= HEIGHT:

                star[0] = random.randint(
                    1,
                    WIDTH-2
                )

                star[1] = 1



# ==========================================================
# ASCII RENDERER
# ==========================================================


class Renderer:


    def __init__(self):

        pass



    def create_screen(self):

        return [
            [
                " "
                for x in range(WIDTH)
            ]
            for y in range(HEIGHT)
        ]



    def draw_border(self, screen):

        pass



    def render(self, screen):

        output = ""

        output += "+" + "-" * WIDTH + "+\n"


        for row in screen:

            output += "|"

            output += "".join(row)

            output += "|\n"


        output += "+" + "-" * WIDTH + "+"


        return output



# ==========================================================
# MAIN GAME CLASS
# ==========================================================


class Game:


    def __init__(self):

        self.player = Player()

        self.stars = StarField()

        self.renderer = Renderer()

        self.bullets = []

        self.enemy_bullets = []

        self.score = 0

        self.level = 1

        self.running = True

        self.paused = False



    def update(self):

        if self.paused:

            return


        self.stars.update()


        for bullet in self.bullets:

            bullet.update()


        self.bullets = [
            b for b in self.bullets
            if b.active
        ]



    def fire(self):

        if self.player.cooldown == 0:

            self.bullets.append(
                Bullet(
                    self.player.x,
                    self.player.y - 1,
                    -1
                )
            )

            self.player.cooldown = 5



    def draw(self):

        screen = self.renderer.create_screen()


        # stars

        for star in self.stars.stars:

            x, y = star

            if (
                0 <= x < WIDTH
                and
                0 <= y < HEIGHT
            ):

                screen[y][x] = "."



        # player

        screen[
            self.player.y
        ][
            self.player.x
        ] = self.player.symbol



        # bullets

        for bullet in self.bullets:

            if bullet.active:

                screen[
                    bullet.y
                ][
                    bullet.x
                ] = "|"



        return self.renderer.render(screen)



# ==========================================================
# SESSION STATE
# ==========================================================


if "game" not in st.session_state:

    st.session_state.game = Game()



game = st.session_state.game
# ==========================================================
# ALIEN SYSTEM
# ==========================================================


class Alien:

    def __init__(self, x, y, row):

        self.x = x
        self.y = y

        self.row = row

        self.alive = True

        # different symbols by alien row

        if row == 0:
            self.symbol = "M"

        elif row == 1:
            self.symbol = "W"

        else:
            self.symbol = "V"



class AlienFleet:


    def __init__(self):

        self.aliens = []

        self.direction = 1

        self.move_timer = 0

        self.create_wave()



    def create_wave(self):

        self.aliens.clear()


        rows = 4

        columns = 10


        for y in range(rows):

            for x in range(columns):

                alien = Alien(
                    6 + x * 4,
                    3 + y * 2,
                    y
                )

                self.aliens.append(alien)



    def alive_count(self):

        return len(
            [
                a for a in self.aliens
                if a.alive
            ]
        )



    def update(self):


        self.move_timer += 1


        # controls alien speed

        if self.move_timer < 8:

            return


        self.move_timer = 0


        hit_edge = False


        for alien in self.aliens:

            if alien.alive:

                if (
                    alien.x <= 2
                    or
                    alien.x >= WIDTH-3
                ):

                    hit_edge = True



        if hit_edge:


            self.direction *= -1


            for alien in self.aliens:

                if alien.alive:

                    alien.y += 1



        else:


            for alien in self.aliens:

                if alien.alive:

                    alien.x += self.direction



    def draw(self, screen):


        for alien in self.aliens:

            if alien.alive:


                if (
                    0 <= alien.x < WIDTH
                    and
                    0 <= alien.y < HEIGHT
                ):

                    screen[
                        alien.y
                    ][
                        alien.x
                    ] = alien.symbol



# ==========================================================
# ADD ALIEN FLEET TO GAME
# ==========================================================


# save original initializer

old_game_init = Game.__init__



def new_game_init(self):

    old_game_init(self)

    self.aliens = AlienFleet()



Game.__init__ = new_game_init



# save original update

old_game_update = Game.update



def new_game_update(self):

    old_game_update(self)

    if not self.paused:

        self.aliens.update()



Game.update = new_game_update



# save original draw

old_game_draw = Game.draw



def new_game_draw(self):

    screen_text = old_game_draw(self)

    return screen_text



Game.draw = new_game_draw
# ==========================================================
# COMBAT SYSTEM
# ==========================================================


def distance_hit(x1, y1, x2, y2):

    return (
        x1 == x2
        and
        y1 == y2
    )



# ==========================================================
# EXTEND GAME UPDATE WITH COMBAT
# ==========================================================


old_combat_update = Game.update



def combat_update(self):

    old_combat_update(self)


    if self.paused:

        return



    # reduce player firing cooldown

    if self.player.cooldown > 0:

        self.player.cooldown -= 1



    # update enemy bullets

    for bullet in self.enemy_bullets:

        bullet.update()



    self.enemy_bullets = [
        b for b in self.enemy_bullets
        if b.active
    ]



    # random alien shooting

    if random.random() < 0.03:


        living = [
            a for a in self.aliens.aliens
            if a.alive
        ]


        if living:

            shooter = random.choice(living)


            self.enemy_bullets.append(
                Bullet(
                    shooter.x,
                    shooter.y + 1,
                    1
                )
            )



    # player bullets hitting aliens

    for bullet in self.bullets:


        for alien in self.aliens.aliens:


            if alien.alive:


                if distance_hit(
                    bullet.x,
                    bullet.y,
                    alien.x,
                    alien.y
                ):

                    alien.alive = False

                    bullet.active = False

                    self.score += 10



    # enemy bullets hitting player

    for bullet in self.enemy_bullets:


        if distance_hit(
            bullet.x,
            bullet.y,
            self.player.x,
            self.player.y
        ):


            bullet.active = False

            self.player.lives -= 1



    # remove dead bullets

    self.bullets = [
        b for b in self.bullets
        if b.active
    ]


    self.enemy_bullets = [
        b for b in self.enemy_bullets
        if b.active
    ]



Game.update = combat_update



# ==========================================================
# EXTEND DRAW FUNCTION
# ==========================================================


old_combat_draw = Game.draw



def combat_draw(self):


    screen = self.renderer.create_screen()



    # stars

    for star in self.stars.stars:

        x, y = star

        if (
            0 <= x < WIDTH
            and
            0 <= y < HEIGHT
        ):

            screen[y][x] = "."



    # aliens

    self.aliens.draw(screen)



    # player

    screen[
        self.player.y
    ][
        self.player.x
    ] = self.player.symbol



    # player bullets

    for bullet in self.bullets:

        if bullet.active:

            if (
                0 <= bullet.y < HEIGHT
                and
                0 <= bullet.x < WIDTH
            ):

                screen[
                    bullet.y
                ][
                    bullet.x
                ] = "|"



    # enemy bullets

    for bullet in self.enemy_bullets:

        if bullet.active:

            if (
                0 <= bullet.y < HEIGHT
                and
                0 <= bullet.x < WIDTH
            ):

                screen[
                    bullet.y
                ][
                    bullet.x
                ] = "!"



    return self.renderer.render(screen)



Game.draw = combat_draw
# ==========================================================
# SHIELD SYSTEM
# ==========================================================


class Shield:


    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.health = 8



    def hit(self):

        self.health -= 1



    def alive(self):

        return self.health > 0



    def symbol(self):

        if self.health >= 6:

            return "#"

        elif self.health >= 3:

            return "+"

        else:

            return "."



class ShieldSystem:


    def __init__(self):

        self.shields = []

        positions = [
            8,
            18,
            28,
            38
        ]


        for x in positions:

            self.shields.append(
                Shield(
                    x,
                    HEIGHT - 7
                )
            )



    def collision(self, bullet):


        for shield in self.shields:


            if shield.alive():

                if (
                    bullet.x == shield.x
                    and
                    bullet.y == shield.y
                ):

                    shield.hit()

                    bullet.active = False

                    return True


        return False



    def draw(self, screen):


        for shield in self.shields:


            if shield.alive():

                screen[
                    shield.y
                ][
                    shield.x
                ] = shield.symbol()



# ==========================================================
# EXPLOSION SYSTEM
# ==========================================================


class Explosion:


    def __init__(self,x,y):

        self.x = x

        self.y = y

        self.life = 3



    def update(self):

        self.life -= 1



    def active(self):

        return self.life > 0



    def draw(self,screen):

        if self.life == 3:

            char = "*"

        elif self.life == 2:

            char = "+"

        else:

            char = "."



        if (
            0 <= self.x < WIDTH
            and
            0 <= self.y < HEIGHT
        ):

            screen[
                self.y
            ][
                self.x
            ] = char



# ==========================================================
# ADD NEW SYSTEMS TO GAME
# ==========================================================


old_system_init = Game.__init__



def system_game_init(self):

    old_system_init(self)


    self.shields = ShieldSystem()


    self.explosions = []


    self.game_over = False


    self.level_complete = False



Game.__init__ = system_game_init



# ==========================================================
# EXTEND UPDATE
# ==========================================================


old_system_update = Game.update



def system_update(self):


    old_system_update(self)



    if self.paused:

        return



    # shield collisions

    for bullet in self.bullets:

        self.shields.collision(
            bullet
        )



    for bullet in self.enemy_bullets:

        self.shields.collision(
            bullet
        )



    # explosions

    for explosion in self.explosions:

        explosion.update()



    self.explosions = [
        e for e in self.explosions
        if e.active()
    ]



    # check aliens reaching player area

    for alien in self.aliens.aliens:


        if alien.alive:

            if alien.y >= HEIGHT - 5:

                self.game_over = True



    # lose condition

    if self.player.lives <= 0:

        self.game_over = True



    # win condition

    if self.aliens.alive_count() == 0:

        self.level_complete = True



Game.update = system_update



# ==========================================================
# EXTEND DRAW WITH SHIELDS/EXPLOSIONS
# ==========================================================


old_system_draw = Game.draw



def system_draw(self):


    screen = self.renderer.create_screen()



    # stars

    for star in self.stars.stars:

        x,y = star

        screen[y][x] = "."



    # shields

    self.shields.draw(screen)



    # aliens

    self.aliens.draw(screen)



    # explosions

    for explosion in self.explosions:

        explosion.draw(screen)



    # player

    screen[
        self.player.y
    ][
        self.player.x
    ] = self.player.symbol



    # bullets

    for bullet in self.bullets + self.enemy_bullets:

        if bullet.active:

            if (
                0 <= bullet.x < WIDTH
                and
                0 <= bullet.y < HEIGHT
            ):

                screen[
                    bullet.y
                ][
                    bullet.x
                ] = "|"



    return self.renderer.render(screen)



Game.draw = system_draw
# ==========================================================
# UFO BONUS SHIP
# ==========================================================


class UFO:


    def __init__(self):

        self.active = False

        self.x = 0

        self.y = 1

        self.direction = 1

        self.timer = 0



    def spawn(self):

        self.active = True

        self.direction = random.choice(
            [-1,1]
        )

        self.timer = 80


        if self.direction == 1:

            self.x = 1

        else:

            self.x = WIDTH-2



    def update(self):


        if not self.active:

            if random.random() < 0.01:

                self.spawn()

            return



        self.x += self.direction


        self.timer -= 1



        if (
            self.x <= 0
            or
            self.x >= WIDTH-1
            or
            self.timer <= 0
        ):

            self.active = False



    def draw(self,screen):


        if self.active:

            screen[
                self.y
            ][
                self.x
            ] = "U"



# ==========================================================
# LEVEL SYSTEM
# ==========================================================


class LevelManager:


    def __init__(self):

        self.level = 1



    def next_level(self):

        self.level += 1



    def enemy_speed(self):

        value = 8 - self.level


        if value < 2:

            value = 2


        return value



# ==========================================================
# EXTEND GAME INITIALIZATION
# ==========================================================


old_level_init = Game.__init__



def level_game_init(self):

    old_level_init(self)


    self.ufo = UFO()

    self.level_manager = LevelManager()

    self.high_score = 0



Game.__init__ = level_game_init



# ==========================================================
# EXTEND UPDATE FOR UFO AND LEVELS
# ==========================================================


old_level_update = Game.update



def level_update(self):


    old_level_update(self)


    if self.paused:

        return



    self.ufo.update()



    # UFO collision

    for bullet in self.bullets:


        if self.ufo.active:


            if (
                bullet.x == self.ufo.x
                and
                bullet.y == self.ufo.y
            ):

                bullet.active = False

                self.ufo.active = False

                self.score += (
                    100 * self.level_manager.level
                )



    # level complete

    if self.level_complete:


        self.level_manager.next_level()


        self.level = (
            self.level_manager.level
        )


        self.score += 250



        self.aliens.create_wave()


        self.level_complete = False



    # update high score

    if self.score > self.high_score:

        self.high_score = self.score



Game.update = level_update



# ==========================================================
# EXTEND DRAW WITH UFO
# ==========================================================


old_level_draw = Game.draw



def level_draw(self):


    screen_text = old_level_draw(self)



    # handled in next renderer expansion

    return screen_text



Game.draw = level_draw
# ==========================================================
# STREAMLIT GAME INTERFACE
# ==========================================================


st.title("👾 ASCII SPACE INVADERS")

st.caption(
    "A retro Space Invaders game built entirely with Python + Streamlit"
)



game = st.session_state.game



# ==========================================================
# CONTROL PANEL
# ==========================================================


controls = st.columns(5)



with controls[0]:

    if st.button("⬅ LEFT"):

        if not game.game_over:

            game.player.move_left()



with controls[1]:

    if st.button("🔥 FIRE"):

        if not game.game_over:

            game.fire()



with controls[2]:

    if st.button("RIGHT ➡"):

        if not game.game_over:

            game.player.move_right()



with controls[3]:

    if st.button("⏯ PAUSE"):

        game.paused = not game.paused



with controls[4]:

    if st.button("🔄 RESET"):

        st.session_state.game = Game()

        st.rerun()



# ==========================================================
# GAME UPDATE
# ==========================================================


if not game.paused and not game.game_over:

    game.update()



# ==========================================================
# DISPLAY
# ==========================================================


display = st.empty()


display.code(
    game.draw()
)



# ==========================================================
# HUD
# ==========================================================


info1, info2, info3 = st.columns(3)



with info1:

    st.metric(
        "Score",
        game.score
    )



with info2:

    st.metric(
        "Lives",
        game.player.lives
    )



with info3:

    st.metric(
        "Level",
        game.level_manager.level
    )



# ==========================================================
# STATUS MESSAGES
# ==========================================================


if game.game_over:

    st.error(
        "GAME OVER - Press RESET"
    )



elif game.level_complete:

    st.success(
        "LEVEL COMPLETE!"
    )



elif game.paused:

    st.warning(
        "GAME PAUSED"
    )



# ==========================================================
# AUTOMATIC FRAME LOOP
# ==========================================================


time.sleep(
    FRAME_DELAY
)


st.rerun()
# ==========================================================
# FINAL RENDERER ENHANCEMENTS
# ==========================================================


old_final_draw = Game.draw



def enhanced_draw(self):


    screen = self.renderer.create_screen()



    # ------------------------------------------------------
    # stars
    # ------------------------------------------------------

    for star in self.stars.stars:

        x, y = star

        if (
            0 <= x < WIDTH
            and
            0 <= y < HEIGHT
        ):

            screen[y][x] = "."



    # ------------------------------------------------------
    # UFO
    # ------------------------------------------------------

    if self.ufo.active:

        if (
            0 <= self.ufo.x < WIDTH
            and
            0 <= self.ufo.y < HEIGHT
        ):

            screen[
                self.ufo.y
            ][
                self.ufo.x
            ] = "U"



    # ------------------------------------------------------
    # shields
    # ------------------------------------------------------

    self.shields.draw(
        screen
    )



    # ------------------------------------------------------
    # aliens
    # ------------------------------------------------------

    self.aliens.draw(
        screen
    )



    # ------------------------------------------------------
    # explosions
    # ------------------------------------------------------

    for explosion in self.explosions:

        explosion.draw(
            screen
        )



    # ------------------------------------------------------
    # player
    # ------------------------------------------------------

    if self.player.lives > 0:

        screen[
            self.player.y
        ][
            self.player.x
        ] = self.player.symbol



    # ------------------------------------------------------
    # bullets
    # ------------------------------------------------------

    for bullet in (
        self.bullets
        +
        self.enemy_bullets
    ):

        if bullet.active:

            if (
                0 <= bullet.x < WIDTH
                and
                0 <= bullet.y < HEIGHT
            ):

                if bullet.direction < 0:

                    screen[
                        bullet.y
                    ][
                        bullet.x
                    ] = "|"

                else:

                    screen[
                        bullet.y
                    ][
                        bullet.x
                    ] = "!"



    return self.renderer.render(
        screen
    )



Game.draw = enhanced_draw



# ==========================================================
# BETTER ALIEN HIT EFFECTS
# ==========================================================


old_collision_update = Game.update



def improved_update(self):


    old_collision_update(self)



    # remove invalid explosions

    self.explosions = [
        e for e in self.explosions
        if e.active()
    ]



Game.update = improved_update



# ==========================================================
# RETRO DISPLAY STYLE
# ==========================================================


st.markdown(
    """
    <style>

    .stCode pre {

        font-size: 18px;

        line-height: 1.05;

    }

    </style>
    """,
    unsafe_allow_html=True
)
# ==========================================================
# FINAL GAME POLISH
# ==========================================================


# ----------------------------------------------------------
# Difficulty scaling
# ----------------------------------------------------------

def update_difficulty(self):

    # make aliens move faster each level

    base = 8 - self.level_manager.level


    if base < 2:

        base = 2


    self.aliens.move_timer = min(
        self.aliens.move_timer,
        base
    )



Game.update_difficulty = update_difficulty



# ----------------------------------------------------------
# Better explosion creation
# ----------------------------------------------------------

def create_explosion(self, x, y):

    self.explosions.append(
        Explosion(
            x,
            y
        )
    )



Game.create_explosion = create_explosion



# ----------------------------------------------------------
# Wrap update for final effects
# ----------------------------------------------------------

old_polish_update = Game.update



def polish_update(self):


    old_polish_update(self)


    self.update_difficulty()



    # keep high score

    if self.score > self.high_score:

        self.high_score = self.score



    # remove dead aliens

    if self.aliens.alive_count() == 0:

        self.level_complete = True



Game.update = polish_update



# ==========================================================
# FINAL HUD ADDITIONS
# ==========================================================


st.divider()


left, right = st.columns(2)


with left:

    st.write(
        f"""
        👾 Aliens Remaining:
        {game.aliens.alive_count()}
        """
    )


with right:

    st.write(
        f"""
        🏆 High Score:
        {game.high_score}
        """
    )



st.caption(
    """
    ASCII Space Invaders
    Built with Python standard library + Streamlit only.
    """
)
