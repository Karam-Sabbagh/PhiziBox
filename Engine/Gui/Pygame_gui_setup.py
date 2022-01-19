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
