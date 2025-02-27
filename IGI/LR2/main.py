import os
from geometric_lib import circle, square

radius = float(os.getenv("RADIUS", 4))
print(f"Circle area: {circle.area(radius)}")

side = float(os.getenv("SIDE", 4))
print(f"Square area: {square.area(side)}")