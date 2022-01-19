class Gui:
    def __init__(self, pygame, pygame_ui_screen, pygame_gui):
        self.pygame_gui = pygame_gui
        self.pygame = pygame

        self.pygame_ui_screen = pygame_ui_screen

        self.screen_width = self.pygame_ui_screen.get_width()
        self.screen_height = self.pygame_ui_screen.get_height()

        self.json_theme_file_path = "Engine/Gui/Theme.json"

        self.ui_manager = self.pygame_gui.UIManager((self.screen_width, self.screen_height), self.json_theme_file_path)

        self.ui_window_exist = False

        self.background = self.pygame.Surface((self.screen_width, self.screen_height))
        self.background.fill(self.ui_manager.get_theme().get_colour("dark_bg"))

        import json
        json_file = open(self.json_theme_file_path)
        self.json_file_variables = json.load(json_file)
        json_file.close()

        self.make_selection_list()

    def make_selection_list(self):
        """
        makes a selection list for the window on the left top corner with a 20 items that's add body buttons
        """
        # pygame gui selection item list for items
        self.selection_items_width = int(self.json_file_variables["selection_list"]["misc"]["list_item_width"])+20

        self.selection_list_length = self.screen_height+2

        # the in the selection list button item and the selection list it self
        # the item width inside the selection list is the selection_list_width - 6 so...

        self.selection_list_width = self.selection_items_width + 6

        self.selection_list_pos_x = self.screen_width+2

        # the buttons in the selection_list = (selection_list_width-6) so if I want the button width to be 64 I should put the selection_list_width = 70

        pygame_selection_list_rect = self.pygame.Rect(0, 0, self.selection_list_width, (self.selection_list_length))
        pygame_selection_list_rect.topright = (self.selection_list_pos_x, 0)

        self.selection_list = self.pygame_gui.elements.UISelectionList(
            pygame_selection_list_rect,
            starting_height=100,
            item_list=[("+", "#Add_body_button")] * 20,
            manager=self.ui_manager,
            allow_multi_select=False,
            anchors={"left": "left",
                     "right": "right",
                     "top": "top",
                     "bottom": "bottom"}
        )

    
    def make_choose_object_window(self):
        """
        makes a window to let the user select the object
        """
        if not self.ui_window_exist:
            self.ui_window = self.pygame_gui.elements.ui_window.UIWindow(self.pygame.Rect(self.screen_width/3, self.screen_height/3, 400, 300),
                                                                         window_display_title="Choose Object",
                                                                         resizable=False,
                                                                         manager=self.ui_manager,
                                                                         object_id="#choose_object_window")
            self.ui_window_exist = True

            self.pygame_gui.elements.UIButton(relative_rect=self.pygame.Rect(0, 0, 90, 70),
                                              text="coming...",
                                              manager=self.ui_manager,
                                              container=self.ui_window,
                                              object_id="#choose_rect_button"
                                              )

    def check_events(self, event):
        """
        :param event: it's from pygame.event.get()
        this function is for checking pygame_gui things
        and it's used for like checking button press or ui window close
        """
        if event.type == self.pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_object_id == "#choose_object_window":
                self.ui_window_exist = False

        self.ui_manager.process_events(event)

    def check_each_selection_list_item(self):
        """
        it just checks the click of each button and item in the selection list that's made with self.make_selection_list
        """
        i = 1
        for each_item in self.selection_list.item_list:
            button_element = each_item["button_element"]
            # sometimes the button is slided up and not really shown so pygame_gui remove this button when it's not seen able and makes it None
            if button_element != None:
                """
                button element have
                held = False
                pressed = False
                is_selected = False
                object_id
                this can be used
                """
                if button_element.pressed and button_element.is_selected:
                    print("button", i, "pressed")
                    self.make_choose_object_window()

                button_rect = button_element.relative_rect
                # the pressed button x position
                button_pos_x = button_rect.x
                # the pressed button y position
                button_pos_y = button_rect.y
            i += 1

    def draw(self, time_delta):
        """
        draws everything about pygame_gui and also does somethings for them
        :param time_delta: it is like time_delta = clock.tick(FPS) so it's just FPS of the screen at the second
        """
        self.check_each_selection_list_item()

        self.ui_manager.update(time_delta)
        self.ui_manager.draw_ui(self.pygame_ui_screen)
