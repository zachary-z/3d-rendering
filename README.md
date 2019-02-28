# 3d-rendering

The wireframe program creates and renders a model of a sphere in three dimensions.  Each point in 3D space is projected onto the screen using the simple projection t(x,y,z) = (x,y) that does not take into account distances from the camera.
  
Each "face" of the sphere is made up of four coplanar points and is drawn as a polygon with each vertex projected onto the screen.  Each face is assigned a color, which is then multiplied by the percentage of light that is reflected off of the polygonal face.  A unit vector normal to the surface is created from the cross product of two edges and the angle between the direction of the light source and the normal vector is calculated using the dot product.  The intensity is calculated using the cosine of the angle and then used if that is positive (otherwise it reflects no light).  The faces are then drawn in the order of distance, with the faces further away being drawn first.

The sphere object itself is created using spherical coordinates to determine points on the sphere.  Coordinates were assigned to faces depending on whether they were next to each other

Here are some pictures of the sphere being rendered:
![3D Sphere](https://raw.githubusercontent.com/zachary-z/3d-rendering/sphere.png)
