import Box2D  # The main library
import math
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody, kinematicBody, edgeShape)

box2d_arguments = [world, polygonShape, circleShape, staticBody, dynamicBody, kinematicBody, edgeShape]


class Phy_Engine:
    def __init__(self, pygame_ui_screen, pygame, gravity):
        self.Box2D = Box2D
        self.PPM = 60  # pixels per meter
        self.box2d_arguments = box2d_arguments

        self.gravity = gravity
        self.do_sleep = True

        self.world = world(gravity=gravity, do_sleep=self.do_sleep)

        # noinspection PyStatementEffect
        self.pygame_ui_screen = pygame_ui_screen
        self.pygame = pygame

        self.SCREEN_WIDTH = (pygame_ui_screen.get_width() - 90)
        self.SCREEN_HEIGHT = pygame_ui_screen.get_height()

        # static: 0
        # edge_chain: 0
        # kinematic: 1
        # dynamic: 2

        self.shapes_colors = {
            staticBody: {"fill_color": (125, 125, 130, 255), "out_line_color": (130, 130, 130, 255)},
            kinematicBody: {"fill_color": (150, 150, 150, 255), "out_line_color": (130, 130, 130, 255)},
            dynamicBody: {"fill_color": (255, 255, 255, 255), "out_line_color": (190, 190, 190, 255)},
            "edge_chain": {"out_line_color": (40, 110, 40, 255)},
            "circle_shape": {"fill_color": (70, 70, 70, 255), "out_line_color": (110, 110, 110, 255)},
            "out_line_color": (190, 190, 190, 255)
        }

        self.bodies_amount = len(self.world.bodies)
        self.hold_able_bodies = []

        # shapes drawing:
        polygonShape.draw = self.polygon_shape_draw
        edgeShape.draw = self.edge_chain_polygon_draw
        circleShape.draw = self.circle_shape_draw

    def generate_polygon_vertices(self, number_of_vertices, scale_x, scale_y):
        """
        this functions creates the vertices of this parameters by using some of math
        :param number_of_vertices: just the number of vertices the angles between them will be calculate automatically
        :param scale_x: number of pixels
        :param scale_y: number of pixels
        :return:
        """
        scale_x /= 2
        scale_y /= 2

        vertices = []
        rotation = math.pi / 4
        for i in range(number_of_vertices):
            r = 2 * math.pi / number_of_vertices * i + rotation  # the '2' here means two of pie
            vertex = (math.cos(r) * scale_x, math.sin(r) * scale_y)  # Rotation + Scaling + Translation
            vertices.append(vertex)

        vertices = self.convert_vertices_to_meters(vertices)

        return vertices

    def generate_rectangle_vertices(self, width, height):
        w = width / 2
        h = height / 2

        vertices = [
            (-w, -h),  # TOPLEFT
            (+w, -h),  # TOPRIGHT
            (+w, h),  # BOTTOMRIGHT
            (-w, +h)  # BOTTOMLEFT
        ]

        vertices = self.convert_vertices_to_meters(vertices)

        return vertices

    def generate_rectangle_vertices_for_edge_chain(self, width, height):
        w = width / 2
        h = height / 2

        vertices = [
            (-w, -h),  # TOPLEFT
            (-w, +h),  # TOPRIGHT
            (+w, +h),  # BOTTOMRIGHT
            (+w, -h),  # BOTTOMLEFT
            (-w, -h)
        ]

        vertices = self.convert_vertices_to_meters(vertices)

        return vertices

    def convert_vertices_to_meters(self, vertices):
        """
        converts vertices positions from pixels to meters
        :param vertices syntax is a list that contains tuples of corner points of a polygon
        """
        for i in range(len(vertices)):
            vertices[i] = tuple((vertices[i][0] / self.PPM, vertices[i][1] / self.PPM))

        return vertices

    def create_dynamic_circle(self, pos_x, pos_y, radius, density, friction, angle=0):
        pos_x = pos_x / self.PPM
        pos_y = (self.SCREEN_HEIGHT - pos_y) / self.PPM
        # Create a dynamic body
        self.circle_body = self.world.CreateDynamicBody(
            position=(pos_x, pos_y), angle=angle
        )
        # add a fixture for the dynamic body
        self.circle_body.CreateCircleFixture(radius=radius / self.PPM, density=density, friction=friction)
        self.hold_able_bodies.append(self.circle_body)

    def create_dynamic_polygon(self, pos_x, pos_y, density, friction, angle=0, number_of_vertices=None, scale=None,
                               box=None):
        if None != box:  # if so this means that the user have chosen to make the polygon a rectangle using the box param
            vertices = self.generate_rectangle_vertices(width=box[0], height=box[1])

        elif None != number_of_vertices and None != scale:  # if so this means that the user have chosen to make the polygon using number of vertices
            vertices = self.generate_polygon_vertices(number_of_vertices=number_of_vertices, scale_x=scale[0],
                                                      scale_y=scale[1])
        else:
            print("you have to pass one of the ways for making a polygon(box or number of vertices with scale)")
            vertices = None

        # we do /PPM for converting the pixels into meters as Box2d requires
        pos_x = pos_x / self.PPM
        # for converting coordinates system from the pc system into the normal life one(that box2d requires)
        pos_y = (self.SCREEN_HEIGHT - pos_y) / self.PPM

        polygon_body = self.world.CreateDynamicBody(
            position=(pos_x, pos_y), angle=angle
        )

        # adding a fixture for the dynamic body to mount it into a shape
        polygon_body.CreatePolygonFixture(vertices=vertices, density=density, friction=friction)

        # this is important for allowing bodies holding
        self.hold_able_bodies.append(polygon_body)

    def create_static_polygon(self, pos_x, pos_y, angle=0, number_of_vertices=None, scale=None, box=None):
        if None != box:  # if so this means that the user have chosen to make the polygon a rectangle using the box param
            vertices = self.generate_rectangle_vertices(width=box[0], height=box[1])

        elif None != number_of_vertices and None != scale:  # if so this means that the user have chosen to make the polygon using number of vertices
            vertices = self.generate_polygon_vertices(number_of_vertices=number_of_vertices, scale_x=scale[0],
                                                      scale_y=scale[1])
        else:
            print("you have to pass one of the ways for making a polygon(box or number of vertices with scale)")
            vertices = None

        pos_x = pos_x / self.PPM
        pos_y = (self.SCREEN_HEIGHT - pos_y) / self.PPM
        angle /= self.PPM

        static_body = self.world.CreateStaticBody(
            position=(pos_x, pos_y),
            shapes=polygonShape(vertices=vertices),
            angle=angle,
        )

    def make_kinematic_polygon(self, pos_x, pos_y, angle=0, number_of_vertices=None, scale=None, box=None, density=1,
                               friction=0.25):
        if None != box:  # if so this means that the user have chosen to make the polygon a rectangle using the box param
            vertices = self.generate_rectangle_vertices(width=box[0], height=box[1])

        elif None != number_of_vertices and None != scale:  # if so this means that the user have chosen to make the polygon using number of vertices
            vertices = self.generate_polygon_vertices(number_of_vertices=number_of_vertices, scale_x=scale[0],
                                                      scale_y=scale[1])
        else:
            print("you have to pass one of the ways for making a polygon(box or number of vertices with scale)")
            vertices = None

        pos_x = pos_x / self.PPM
        pos_y = (self.SCREEN_HEIGHT - pos_y) / self.PPM
        angle /= self.PPM

        kinematic_body = self.world.CreateKinematicBody(
            position=(pos_x, pos_y), angle=angle
        )

        # adding a fixture for the dynamic body to mount it into a shape
        kinematic_body.CreatePolygonFixture(vertices=vertices, density=density, friction=friction)

        self.hold_able_bodies.append(kinematic_body)
