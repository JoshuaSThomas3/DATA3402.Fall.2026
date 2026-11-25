
import math


# Canvas class based on Lecture 9
class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        # Only draw points that fit on the canvas
        row = int(round(row))
        col = int(round(col))

        if 0 <= row < self.height and 0 <= col < self.width:
            self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]

    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]

    def v_line(self, x, y, h, char='*'):
        for i in range(h):
            self.set_pixel(x + i, y, char)

    def h_line(self, x, y, w, char='*'):
        for i in range(w):
            self.set_pixel(x, y + i, char)

    def line(self, x1, y1, x2, y2, char='*'):
        # Draw points between the two endpoints
        steps = int(max(abs(x2 - x1), abs(y2 - y1)))

        if steps == 0:
            self.set_pixel(x1, y1, char)
            return

        for i in range(steps + 1):
            t = i / steps
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            self.set_pixel(x, y, char)

    def display(self):
        for row in self.data:
            print(''.join(row))


# Base class for the different shapes
class Shape:
    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

    def perimeter_points(self):
        raise NotImplementedError

    def is_inside(self, x, y):
        raise NotImplementedError

    def overlaps(self, other):
        # Check sampled perimeter points from both shapes
        for x, y in self.perimeter_points():
            if other.is_inside(x, y):
                return True

        for x, y in other.perimeter_points():
            if self.is_inside(x, y):
                return True

        return False

    def paint(self, canvas):
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, length, width, x, y):
        self.__length = length
        self.__width = width
        self.__x = x
        self.__y = y

    def area(self):
        return self.__length * self.__width

    def perimeter(self):
        return 2 * (self.__length + self.__width)

    def get_length(self):
        return self.__length

    def get_width(self):
        return self.__width

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def perimeter_points(self):
        points = []

        for i in range(4):
            t = i / 4
            points.append((self.__x + t * self.__length,
                           self.__y))
            points.append((self.__x + self.__length,
                           self.__y + t * self.__width))
            points.append((self.__x + (1 - t) * self.__length,
                           self.__y + self.__width))
            points.append((self.__x,
                           self.__y + (1 - t) * self.__width))

        return points

    def is_inside(self, x, y):
        return (self.__x <= x <= self.__x + self.__length
                and self.__y <= y <= self.__y + self.__width)

    def paint(self, canvas):
        # Draw the four sides of the rectangle
        x = self.__x
        y = self.__y
        length = self.__length
        width = self.__width

        canvas.line(y, x, y, x + length, '#')
        canvas.line(y + width, x, y + width, x + length, '#')
        canvas.line(y, x, y + width, x, '#')
        canvas.line(y, x + length, y + width, x + length, '#')


class Circle(Shape):
    def __init__(self, radius, x, y):
        self.__radius = radius
        self.__x = x
        self.__y = y

    def area(self):
        return math.pi * self.__radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.__radius

    def get_radius(self):
        return self.__radius

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def perimeter_points(self):
        points = []

        for i in range(16):
            angle = 2 * math.pi * i / 16
            x = self.__x + self.__radius * math.cos(angle)
            y = self.__y + self.__radius * math.sin(angle)
            points.append((x, y))

        return points

    def is_inside(self, x, y):
        distance = (x - self.__x)**2 + (y - self.__y)**2
        return distance <= self.__radius**2

    def paint(self, canvas):
        # Use small line segments around the circle
        for i in range(64):
            a1 = 2 * math.pi * i / 64
            a2 = 2 * math.pi * (i + 1) / 64

            x1 = self.__x + self.__radius * math.cos(a1)
            y1 = self.__y + self.__radius * math.sin(a1)
            x2 = self.__x + self.__radius * math.cos(a2)
            y2 = self.__y + self.__radius * math.sin(a2)

            canvas.line(y1, x1, y2, x2, 'O')


class Triangle(Shape):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.__points = [(x1, y1), (x2, y2), (x3, y3)]

    def get_points(self):
        return self.__points.copy()

    def get_x(self):
        return self.__points[0][0]

    def get_y(self):
        return self.__points[0][1]

    def area(self):
        (x1, y1), (x2, y2), (x3, y3) = self.__points
        return abs(x1*(y2-y3) + x2*(y3-y1)
                   + x3*(y1-y2)) / 2

    def perimeter(self):
        total = 0

        for i in range(3):
            p1 = self.__points[i]
            p2 = self.__points[(i + 1) % 3]
            total += math.dist(p1, p2)

        return total

    def perimeter_points(self):
        points = []

        for side in range(3):
            start = self.__points[side]
            end = self.__points[(side + 1) % 3]

            for i in range(5):
                t = i / 5
                x = start[0] + t * (end[0] - start[0])
                y = start[1] + t * (end[1] - start[1])
                points.append((x, y))

        return points

    def is_inside(self, x, y):
        # Compare areas of the three smaller triangles
        p1, p2, p3 = self.__points

        def sign(a, b, c):
            return ((a[0] - c[0]) * (b[1] - c[1])
                    - (b[0] - c[0]) * (a[1] - c[1]))

        point = (x, y)
        d1 = sign(point, p1, p2)
        d2 = sign(point, p2, p3)
        d3 = sign(point, p3, p1)

        negative = d1 < 0 or d2 < 0 or d3 < 0
        positive = d1 > 0 or d2 > 0 or d3 > 0

        return not (negative and positive)

    def paint(self, canvas):
        # Connect the three corners with lines
        for i in range(3):
            x1, y1 = self.__points[i]
            x2, y2 = self.__points[(i + 1) % 3]
            canvas.line(y1, x1, y2, x2, '+')


class CompoundShape(Shape):
    def __init__(self, shapes):
        self.shapes = shapes

    def paint(self, canvas):
        # Paint every shape in the group
        for shape in self.shapes:
            shape.paint(canvas)

# Exercise 11 - RasterDrawing class

class RasterDrawing:
    def __init__(self):
        # Store the shapes by their names
        self.shapes = {}
        self.shape_names = []

    def add_shape(self, shape, name=None):
        # Give the shape a name if one was not provided
        if name is None:
            name = "shape_" + str(len(self.shapes))

        # Add the shape to the dictionary
        self.shapes[name] = shape

        if name not in self.shape_names:
            self.shape_names.append(name)

    def remove_shape(self, name):
        # Remove a shape if it exists
        if name in self.shapes:
            del self.shapes[name]
            self.shape_names.remove(name)
        else:
            print("Shape not found.")

    def paint(self, canvas):
        # Draw every shape stored in the drawing
        for name in self.shape_names:
            shape = self.shapes[name]
            shape.paint(canvas)

    def update(self, canvas):
        # Clear the canvas and draw the shapes again
        canvas.clear_canvas()
        self.paint(canvas)

    
    # Save the drawing to a JSON file
    def save(self, filename):
        import json

        saved_shapes = []

        # Go through each shape in the drawing
        for name in self.shape_names:
            shape = self.shapes[name]

            if isinstance(shape, Rectangle):
                info = {
                    "name": name,
                    "type": "Rectangle",
                    "length": shape.get_length(),
                    "width": shape.get_width(),
                    "x": shape.get_x(),
                    "y": shape.get_y()
                }

            elif isinstance(shape, Circle):
                info = {
                    "name": name,
                    "type": "Circle",
                    "radius": shape.get_radius(),
                    "x": shape.get_x(),
                    "y": shape.get_y()
                }

            elif isinstance(shape, Triangle):
                info = {
                    "name": name,
                    "type": "Triangle",
                    "points": shape.get_points()
                }

            else:
                raise ValueError("Unsupported shape type")

            saved_shapes.append(info)

        # Write the data to a file
        with open(filename, "w") as file:
            json.dump(saved_shapes, file, indent=4)


    # Load a drawing from a JSON file
    @classmethod
    def load(cls, filename):
        import json

        # Read the saved shape information
        with open(filename, "r") as file:
            saved_shapes = json.load(file)

        drawing = cls()

        # Recreate each shape using its saved information
        for info in saved_shapes:

            if info["type"] == "Rectangle":
                shape = Rectangle(
                    info["length"],
                    info["width"],
                    info["x"],
                    info["y"]
                )

            elif info["type"] == "Circle":
                shape = Circle(
                    info["radius"],
                    info["x"],
                    info["y"]
                )

            elif info["type"] == "Triangle":
                p = info["points"]

                shape = Triangle(
                    p[0][0], p[0][1],
                    p[1][0], p[1][1],
                    p[2][0], p[2][1]
                )

            else:
                raise ValueError("Unknown shape type")

            drawing.add_shape(shape, info["name"])

        return drawing
import json

## Created Raster drawing class to store multiple shapes
## Using a dictionary I organized the shapes by their names
## Created add_shape and remove_shape methods to add and remove shapes from the drawing.
# Paint method will draw each stored shape on the canvas while the update method wil clear the canvas before drawing.
# In my test I removed the circle and displayed the result to see if it works.





# Exercise 11 - RasterDrawing class

class RasterDrawing:
    def __init__(self):
        # Store the shapes by their names
        self.shapes = {}
        self.shape_names = []

    def add_shape(self, shape, name=None):
        # Give the shape a name if one was not provided
        if name is None:
            name = "shape_" + str(len(self.shapes))

        # Add the shape to the dictionary
        self.shapes[name] = shape

        if name not in self.shape_names:
            self.shape_names.append(name)

    def remove_shape(self, name):
        # Remove a shape if it exists
        if name in self.shapes:
            del self.shapes[name]
            self.shape_names.remove(name)
        else:
            print("Shape not found.")

    def paint(self, canvas):
        # Draw every shape stored in the drawing
        for name in self.shape_names:
            shape = self.shapes[name]
            shape.paint(canvas)

    def update(self, canvas):
        # Clear the canvas and draw the shapes again
        canvas.clear_canvas()
        self.paint(canvas)

    @staticmethod
    def _shape_to_dict(shape):
        if isinstance(shape, Rectangle):
            return {
                "type": "Rectangle",
                "length": shape.get_length(),
                "width": shape.get_width(),
                "x": shape.get_x(),
                "y": shape.get_y()
            }

        if isinstance(shape, Circle):
            return {
                "type": "Circle",
                "radius": shape.get_radius(),
                "x": shape.get_x(),
                "y": shape.get_y()
            }

        if isinstance(shape, Triangle):
            return {
                "type": "Triangle",
                "points": shape.get_points()
            }

        if isinstance(shape, CompoundShape):
            return {
                "type": "CompoundShape",
                "shapes": [
                    RasterDrawing._shape_to_dict(s)
                    for s in shape.shapes
                ]
            }

        raise TypeError("Unsupported shape type")

    # Recreate a shape from its saved information
    @staticmethod
    def _dict_to_shape(data):
        kind = data["type"]

        if kind == "Rectangle":
            return Rectangle(
                data["length"], data["width"],
                data["x"], data["y"]
            )

        if kind == "Circle":
            return Circle(
                data["radius"], data["x"], data["y"]
            )

        if kind == "Triangle":
            p = data["points"]
            return Triangle(
                p[0][0], p[0][1],
                p[1][0], p[1][1],
                p[2][0], p[2][1]
            )

        if kind == "CompoundShape":
            shapes = [
                RasterDrawing._dict_to_shape(s)
                for s in data["shapes"]
            ]
            return CompoundShape(shapes)

        raise ValueError("Unknown shape type: " + str(kind))

    # Save the names and information for every shape
    def save(self, filename):
        records = []

        for name in self.shape_names:
            records.append({
                "name": name,
                "shape": self._shape_to_dict(self.shapes[name])
            })

        with open(filename, "w") as f:
            json.dump(records, f, indent=2)

    # Load a drawing from its saved JSON file
    @classmethod
    def load(cls, filename):
        with open(filename, "r") as f:
            records = json.load(f)

        drawing = cls()

        for item in records:
            shape = cls._dict_to_shape(item["shape"])
            drawing.add_shape(shape, item["name"])

        return drawing
