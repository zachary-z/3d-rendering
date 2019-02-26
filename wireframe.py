from Vector import *
import pygame
import random
import math

'''
def project(point):
    return (int(point[0]), int(point[1]))

class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.array = [a,b]
    def draw(self, screen):
        a = project(self.a)
        b = project(self.b)
        pygame.draw.line(screen, (50,50,50), a, b, 1)

class Face:
    def __init__(self, vertices, edges):
        self.v = vertices
        self.e = edges
    def draw(self, screen, color, light_direction=vec(-1,-1,-1)):
        for vertex in self.v:
            pygame.draw.circle(screen, (0,0,0), project(v), 2)
        for edge in self.e:
            e.draw(screen)
        # Lighting calculations
        normal = ((self.v[1]-self.v[0])^(self.v[2]-self.v[0])).normalize()
        angle = math.acos((light_direction*normal)/abs(light_direction))
        brightness = math.sin(angle)
        color = (brightness*color[0], brightness*color[1], brightness*color[2])
        # Drawing the face
        vertices = [projected(v) for v in self.v]
        pygame.draw.polygon(screen, color, vertices, 0)

class Wireframe:
    def __init__(self, vertices, edges, faces):
        self.v = vertices
        self.e = edges
        self.f = faces
    def translate(self, vector):
        for vertex in self.v:
            vertex = vertex + vector
    def scale(self, center, scalar):
        for vertex in self.v:
            vertex[0] = center[0]+scalar*(vertex[0]-center[0])
            vertex[1] = center[1]+scalar*(vertex[1]-center[1])
            vertex[2] = scalar*vertex[2]
    def center(self):
        return sum(self.v)/len(self.v)
'''

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def project(self):
        center = (200,200)
        z_effect = min(1.1**(self.z/50), 10)
        x = int(center[0]+z_effect*(self.x-center[0]))
        y = 400-int(center[1]+z_effect*(self.y-center[1]))
        x2 = int(self.x)
        y2 = int(400-self.y)
        return (x2, y2)
    def draw(self, screen):
        pygame.draw.circle(screen, (220,220,220), self.project(), 2)

class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def draw(self, screen):
        pygame.draw.line(screen, (200,200,200), self.a.project(), self.b.project(), 2)

class Face:
    def __init__(self, vertices, edges, color=(255,0,0)):
        self.e = edges
        self.v = vertices
        self.color = color
    def center(self):
        x = sum([v.x for v in self.v])/len(self.v)
        y = sum([v.y for v in self.v])/len(self.v)
        z = sum([v.z for v in self.v])/len(self.v)
        return Point(x,y,z)
    def normal(self):
        edge1 = vec(self.v[0].x-self.v[1].x, self.v[0].y-self.v[1].y, self.v[0].z-self.v[1].z)
        edge2 = vec(self.v[2].x-self.v[1].x, self.v[2].y-self.v[1].y, self.v[2].z-self.v[1].z)
        return (edge1^edge2).normalize()
    def draw(self, screen, vector):
        # Calculate lighting
        light_direction = vector.normalize()
        normal = self.normal()
        intensity = max(normal*light_direction, 0)
        color = (self.color[0]*intensity,
                 self.color[1]*intensity,
                 self.color[2]*intensity)
        pygame.draw.polygon(screen, color, [v.project() for v in self.v], 0)
        

class Wireframe:
    def __init__(self, edges):
        self.v = [e.a for e in edges]
        self.v = self.v + [e.b for e in edges]
        self.v = list(set(self.v))
        self.e = edges
    def add_vertices(self, vertices):
        for p in vertices:
            self.v.append(p)
        self.v = list(set(self.v))
    def add_edges(self, edges):
        for e in edges:
            self.e.append(e)
            self.v.append(e.a)
            self.v.append(e.b)
        self.v = list(set(self.v))
        self.e = list(set(self.e))
    def draw(self, screen):
        for p in self.v:
            p.draw(screen)
        for e in self.e:
            e.draw(screen)

    def translate(self, vec):
        for p in self.v:
            p.x += vec.x
            p.y += vec.y
            p.z += vec.z
    def scale(self, center, scale):
        for p in self.v:
            p.x = center.x+scale*(p.x-center.x)
            p.y = center.y+scale*(p.y-center.y)
            p.z = center.z+scale*(p.z-center.z)
    def center(self):
        x = sum([p.x for p in self.v])/len(self.v)
        y = sum([p.y for p in self.v])/len(self.v)
        z = sum([p.z for p in self.v])/len(self.v)
        return Point(x,y,z)
    def rotate(self, axis, center, amount):
       for p in self.v:
           x = p.x-center.x
           y = p.y-center.y
           z = p.z-center.z
           if axis == 'x':
               radius = math.sqrt(y*y + z*z)
               theta = math.atan2(y, z) + amount
               p.z = center.z+radius*math.cos(theta)
               p.y = center.y+radius*math.sin(theta)
           if axis == 'y':
                radius = math.sqrt(x*x + z*z)
                theta = math.atan2(x, z) + amount
                p.z = center.z+radius*math.cos(theta)
                p.x = center.x+radius*math.sin(theta)
           if axis == 'z':
                radius = math.sqrt(x*x + y*y)
                theta = math.atan2(y, x) + amount
                p.x = center.x+radius*math.cos(theta)
                p.y = center.y+radius*math.sin(theta)

class Solid:
    def __init__(self, faces):
        self.f = faces
        self.e = list(set([e for f in self.f for e in f.e]))
        self.v = list(set([e.a for e in self.e]))+list(set([e.b for e in self.e]))
    def add_faces(self, faces):
        self.f = list(set([self.f+faces]))
        self.e = list(set([e for f in self.f for e in f.e]))
        self.v = list(set([e.a for e in self.e]))+list(set([e.b for e in self.e]))
    def draw(self, screen, vector):
        self.f = sorted(self.f, key=lambda x: x.center().z, reverse=False)
        for f in self.f:
            f.draw(screen, vector)
    def translate(self, vec):
        for p in self.v:
            p.x += vec.x
            p.y += vec.y
            p.z += vec.z
    def scale(self, center, scale):
        for p in self.v:
            p.x = center.x+scale*(p.x-center.x)
            p.y = center.y+scale*(p.y-center.y)
            p.z = center.z+scale*(p.z-center.z)
    def center(self):
        x = sum([p.x for p in self.v])/len(self.v)
        y = sum([p.y for p in self.v])/len(self.v)
        z = sum([p.z for p in self.v])/len(self.v)
        return Point(x,y,z)
    def rotate(self, axis, center, amount):
       for p in self.v:
           x = p.x-center.x
           y = p.y-center.y
           z = p.z-center.z
           if axis == 'x':
               radius = math.sqrt(y*y + z*z)
               theta = math.atan2(y, z) + amount
               p.z = center.z+radius*math.cos(theta)
               p.y = center.y+radius*math.sin(theta)
           if axis == 'y':
                radius = math.sqrt(x*x + z*z)
                theta = math.atan2(x, z) + amount
                p.z = center.z+radius*math.cos(theta)
                p.x = center.x+radius*math.sin(theta)
           if axis == 'z':
                radius = math.sqrt(x*x + y*y)
                theta = math.atan2(y, x) + amount
                p.x = center.x+radius*math.cos(theta)
                p.y = center.y+radius*math.sin(theta)
    

class Viewer:
    def __init__(self):
        self.screen = pygame.display.set_mode((400,400))
        pygame.display.set_caption(' Drag to rotate, scroll to zoom, arrow keys to move')
        # Colors
        self.background_color = (0,0,0)
        self.vertex_color = (220,220,220)
        self.edge_color = (200,200,200)
        # Other stuff
        self.wireframes = {}
        self.solids = {}
        self.keybindings = {# Translation
                            pygame.K_LEFT: (lambda x,y: x.translate_all(Point(-10,0,0))),
                            pygame.K_RIGHT: (lambda x,y: x.translate_all(Point(10,0,0))),
                            pygame.K_DOWN: (lambda x,y: x.translate_all(Point(0,-10,0))),
                            pygame.K_UP: (lambda x,y: x.translate_all(Point(0,10,0))),
                            # Scaling
                            pygame.K_EQUALS: (lambda x,y: x.scale_all(y, 1.25)),
                            pygame.K_MINUS: (lambda x,y: x.scale_all(y, 0.8)),
                            # Rotation
                            pygame.K_q: (lambda x,y: x.rotate_all('x', -0.1)),
                            pygame.K_w: (lambda x,y: x.rotate_all('x', 0.1)),
                            pygame.K_a: (lambda x,y: x.rotate_all('y', -0.1)),
                            pygame.K_s: (lambda x,y: x.rotate_all('y', 0.1)),
                            pygame.K_z: (lambda x,y: x.rotate_all('z', -0.1)),
                            pygame.K_x: (lambda x,y: x.rotate_all('z', 0.1))
                            }
    def run(self):
        done = False
        lastmousepos = Point(pygame.mouse.get_pos()[0], 400-pygame.mouse.get_pos()[1], 0)
        scale = 1
        dy = 4
        dx = 0
        lightv = vec(1,1,1)
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.keybindings:
                        mouse = Point(pygame.mouse.get_pos()[0], 400-pygame.mouse.get_pos()[1], 0)
                        self.keybindings[event.key](self, mouse)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        mouse = Point(pygame.mouse.get_pos()[0], 400-pygame.mouse.get_pos()[1], 0)
                        self.scale_all(mouse, 1.03)
                        scale *= 0.97
                    if event.button == 5:
                        mouse = Point(pygame.mouse.get_pos()[0], 400-pygame.mouse.get_pos()[1], 0)
                        self.scale_all(mouse, 0.97)
                        scale *= 1.03
            self.screen.fill(self.background_color)
            mousepos = Point(pygame.mouse.get_pos()[0], 400-pygame.mouse.get_pos()[1], 0)
            if pygame.mouse.get_pressed()[0]:
                dy = mousepos.y-lastmousepos.y
                dx = mousepos.x-lastmousepos.x
                self.rotate_all('y', dx*0.01*scale)
                self.rotate_all('x', dy*0.01*scale)
            else:
                self.rotate_all('y', dx*0.01)
                self.rotate_all('x', dy*0.01)
            lastmousepos = Point(pygame.mouse.get_pos()[0], 400-pygame.mouse.get_pos()[1], 0)
            dy *= 0.97
            dx *= 0.97

            angle = math.atan2(lightv[1], lightv[0])+0.1
            lightv = vec(math.cos(angle), math.sin(angle), 1)
            
            for w in self.wireframes:
                self.wireframes[w].draw(self.screen)
            for s in self.solids:
                self.solids[s].draw(self.screen, lightv)
            pygame.display.update()

    def translate_all(self, vec):
        for w in self.wireframes:
            self.wireframes[w].translate(vec)
        for s in self.solids:
            self.solids[s].translate(vec)
    def scale_all(self, center, scale):
        for w in self.wireframes:
            self.wireframes[w].scale(center, scale)
        for s in self.solids:
            self.solids[s].scale(center, scale)
    def rotate_all(self, axis, amount):
        for w in self.wireframes:
            self.wireframes[w].rotate(axis, self.wireframes[w].center(), amount)
        for s in self.solids:
            self.solids[s].rotate(axis, self.solids[s].center(), amount)
        
        

# Vertices and edges of a cube

vertices = [Point(i,j,k) for i in [100,300] for j in [100,300] for k in [-100,100]]
edges = []
edges = edges + [Edge(vertices[0],vertices[4]), Edge(vertices[1],vertices[5])]
edges = edges + [Edge(vertices[2],vertices[6]), Edge(vertices[3],vertices[7])]
edges = edges + [Edge(vertices[0],vertices[1]), Edge(vertices[2],vertices[3])]
edges = edges + [Edge(vertices[4],vertices[5]), Edge(vertices[6],vertices[7])]
edges = edges + [Edge(vertices[0],vertices[2]), Edge(vertices[1],vertices[3])]
edges = edges + [Edge(vertices[4],vertices[6]), Edge(vertices[5],vertices[7])]
cube = Wireframe(edges)

vertices = [[150,O,o] for o in range(17) for O in range(32)] # Sphere "vertices"

# vertices = vertices + [[200,0,0],[200,0,8]] # Poles

def sphere_convert(rho,theta,phi):
    t = theta*math.pi/32
    p = phi*math.pi/32
    x = rho*math.cos(t)*math.sin(p)
    y = rho*math.sin(t)*math.sin(p)
    z = rho*math.cos(p)
    return Point(200+x,200+y,z)
'''
vertices2 = [sphere_convert(*vertices[i]) for i in range(len(vertices))]
edges = []
for v in range(len(vertices)):
    # edges.append(Edge(Point(200,200,0), vertices2[v]))
    for w in range(len(vertices)):
        if (vertices[v][1]-vertices[w][1]) % 32 == 1 and vertices[v][2] == vertices[w][2]: # latitude
            edges.append(Edge(vertices2[v], vertices2[w]))
        if vertices[v][2]-vertices[w][2] == 1 and vertices[v][1] == vertices[w][1]: # longitude
            edges.append(Edge(vertices2[v], vertices2[w]))
sphere = Wireframe(edges)
'''

vertices3 = [[[150,O,o] for O in range(64)] for o in range(33)]
vertices4 = [[sphere_convert(*vertices3[i][j]) for j in range(len(vertices3[0]))] for i in range(len(vertices3))]

'''
#                    4       8       12      16
projection = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 1
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 4
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 8
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0],
              [0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0,0], # 12
              [0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0],
              [0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0], # 16
              [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
              [0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0],
              [0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0],
              [0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0,0], # 20
              [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 24
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 28
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]] # 32
'''              
       
faces = []
for i in range(len(vertices3)-1):
    for j in range(len(vertices3[0])):
        a1 = vertices4[i][j]
        a2 = vertices4[i][(j+1)%len(vertices3[0])]
        b2 = vertices4[i+1][(j+1)%len(vertices3[0])]
        b1 = vertices4[i+1][j]
        if j < 7:
            color = (255,0,0)
        elif j < 15:
            color = (255,128,0)
        elif j < 23:
            color = (255,255,0)
        elif j < 31:
            color = (0,255,0)
        elif j < 39:
            color = (0,0,255)
        elif j < 47:
            color = (128,0,255)
        elif j < 55:
            color = (200,100,30)
        else:
            color = (255,255,255)
        faces.append(Face([a1,a2,b2,b1],[Edge(a1,a2),Edge(a2,b2),Edge(b2,b1),Edge(b1,a1)], color))
ball = Solid(faces)
    
'''
faces = []
edges = [Edge(Point(100,100,-100),Point(100,300,-100)),
         Edge(Point(100,100,-100),Point(300,100,-100)),
         Edge(Point(300,300,-100),Point(100,300,-100)),
         Edge(Point(300,300,-100),Point(300,100,-100)),
         Edge(Point(100,100,100),Point(100,300,100)),
         Edge(Point(100,100,100),Point(300,100,100)),
         Edge(Point(300,300,100),Point(100,300,100)),
         Edge(Point(300,300,100),Point(300,100,100)),
         Edge(Point(100,100,-100),Point(100,100,100)),
         Edge(Point(300,100,-100),Point(300,100,100)),
         Edge(Point(100,300,-100),Point(100,300,100)),
         Edge(Point(300,300,-100),Point(300,300,100))]
faces.append()
'''

viewer = Viewer()
# viewer.wireframes['cube'] = cube
# viewer.wireframes['sphere'] = sphere
viewer.solids['ball'] = ball
viewer.run()
        
