import pygame
from Engine import Physics_Engine
from Engine.Gui import Pygame_gui_setup
import pygame_gui

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

pygame_ui_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame_ui_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PhiziBox")

background_colour = (35, 35, 35)
pygame_ui_screen.fill(background_colour)

clock = pygame.time.Clock()

# game setup here:
Phy_Eng = Physics_Engine.Phy_Engine(pygame_ui_screen, pygame, gravity=(0, -10))
Phy_Eng.setup_world()

pygame_gui_setup = Pygame_gui_setup.Gui(pygame, pygame_ui_screen, pygame_gui)

start_tick = pygame.time.get_ticks()
seconds = 0

if __name__ == "__main__":
    # -- FOR SPAWNING BODIES IN THE GUI --
    # for default pressing properties:
    check_keys = [pygame.K_p, pygame.K_c, pygame.K_k, pygame.K_r, pygame.K_n]
    released_press_keys = {}
    pressed_mouse_right_click = False

    on_press_keys = {}
    pressed_keys = {}

    for each_key in check_keys:
        released_press_keys[each_key] = False
        on_press_keys[each_key] = False
        pressed_keys[each_key] = False

    def check_released_press_keys():
        pygame_pressed_keys = pygame.key.get_pressed()

        for check_key in check_keys:
            # check if the key is pressed
            if pygame_pressed_keys[check_key]:
                on_press_keys[check_key] = True
                pressed_keys[check_key] = True
            else:
                on_press_keys[check_key] = False

            # if the key is not on pressing now and it did press before this means that we have a key release.
            if not on_press_keys[check_key] and pressed_keys[check_key]:
                pressed_keys[check_key] = False
                on_press_keys[check_key] = False
                released_press_keys[check_key] = True

    def spawn_bodies_with_keys():
        check_released_press_keys()
        pygame_pressed_keys = pygame.key.get_pressed()
        global pressed_mouse_right_click

        # mouse click checking
        if pygame.mouse.get_pressed()[0]:
            mouse_y = (SCREEN_HEIGHT - pygame.mouse.get_pos()[1])
            mouse_x = pygame.mouse.get_pos()[0]
            # check if clicked inside of a polygon
            for body in Phy_Eng.hold_able_bodies:
                hit = Phy_Eng.body_check_hit(body, (mouse_x, mouse_y))
                if hit == True:
                    body.awake = True
                    Phy_Eng.set_body_position(body, (mouse_x, mouse_y))
                    body.linearVelocity = Phy_Eng.Box2D.b2Vec2(0, 0)
                    body.angularVelocity = 0
                    break

        pressed_mouse_right_click = pressed_mouse_right_click
        if pygame.mouse.get_pressed()[2]:
            pressing_mouse_right_click = True
            pressed_mouse_right_click = True
        else:
            pressing_mouse_right_click = False

        # for deleting a dynamic body
        if pressing_mouse_right_click == False and pressed_mouse_right_click == True:
            mouse_y = (SCREEN_HEIGHT - pygame.mouse.get_pos()[1])
            mouse_x = pygame.mouse.get_pos()[0]
            # check if clicked inside of a polygon
            for body in Phy_Eng.hold_able_bodies:
                hit = Phy_Eng.body_check_hit(body, (mouse_x, mouse_y))
                if hit == True:
                    Phy_Eng.destroy_body(body)
                    break

            pressed_mouse_right_click = False

        if pygame_pressed_keys[pygame.K_s]:
            for i in range(3):
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                # smallest circle radius can be around 1.0000001
                Phy_Eng.create_dynamic_circle(pos_x=mouse_x,
                                              pos_y=mouse_y, radius=1.0000001, density=0.75, friction=0)

        if released_press_keys[pygame.K_c]:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            # smallest circle radius can be 1.0000001
            Phy_Eng.create_dynamic_circle(mouse_x,
                                          mouse_y, radius=40, angle=0, density=1, friction=0.05)
            # you should do this to give it that its pressed now if you don't do this it will be true and say that the key is pressed forever
            released_press_keys[pygame.K_c] = False

        # keyboard keys checking
        # make a polygon when mouse right button is clicked
        if released_press_keys[pygame.K_p]:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            scale_x, scale_y = 130, 130
            Phy_Eng.create_dynamic_polygon(pos_x=mouse_x,
                                           pos_y=mouse_y, number_of_vertices=5, scale=(scale_x, scale_y), angle=0, density=1.5, friction=0.1)
            # you should do this to give it that its pressed now if you don't do this it will be true and say that the key is pressed forever
            released_press_keys[pygame.K_p] = False

        if released_press_keys[pygame.K_r]:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]

            rect_width = 70
            rect_height = 130

            Phy_Eng.create_dynamic_polygon(pos_x=mouse_x,
                                           pos_y=mouse_y, number_of_vertices=4, box=(rect_width, rect_height), angle=0, density=1.5, friction=0.1)
            # you should do this to give it that its pressed now if you don't do this it will be true and say that the key is pressed forever
            released_press_keys[pygame.K_r] = False

        if released_press_keys[pygame.K_k]:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]

            Phy_Eng.make_kinematic_polygon(pos_x=mouse_x, pos_y=mouse_y, box=(40, 90))

            released_press_keys[pygame.K_k] = False

        if released_press_keys[pygame.K_n]:
            Phy_Eng.reset_world()

            released_press_keys[pygame.K_n] = False

    # text:
    pygame.font.init()
    font = pygame.font.SysFont("arial", 25)
    text_color = (180, 180, 180)

    FPS = 60

    running_game = True

    while running_game:
        time_delta = clock.tick(FPS)
        seconds = (pygame.time.get_ticks() - start_tick) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False

            pygame_gui_setup.check_events(event)

        pygame_ui_screen.fill(background_colour)

        # drawing here:

        spawn_bodies_with_keys()

        fps = clock.get_fps()

        # drawing here:
        for body in (Phy_Eng.world.bodies):
            # The body gives us the position and angle of its shapes
            for fixture in body.fixtures:
                fixture.shape.draw(fixture.shape, body=body, fixture=fixture)

        if fps == 0:
            fps = 1

        Phy_Eng.step(fps)
        # if the fps is not set do: Phy_Eng.world.Step(1 / fps, 20, 20)

        # show FPS text

        text_seconds = font.render(("FPS: " + (str(int(fps)))), True, (text_color))
        pygame_ui_screen.blit(text_seconds, (20, 15))

        # show bodies amount
        text_seconds = font.render(("Bodies Amount: " + (str(int(Phy_Eng.bodies_amount)))), True, (text_color))
        pygame_ui_screen.blit(text_seconds, (20, 50))

        pygame_gui_setup.draw(time_delta)

        pygame.display.flip()
        pygame.display.update()

    pygame.quit()
