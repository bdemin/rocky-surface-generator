rad = 5;

[sphere_x, sphere_y, sphere_z] = sphere;
sphere_x = sphere_x*rad; sphere_y = sphere_y*rad; sphere_z = sphere_z*rad;

plane_norm = [0, 0, 1];
a = plane_norm(1); b = plane_norm(2); c = plane_norm(3);
% normal = normal/norm(normal);
plane_point = [4.5, 4.5, -1];


% syms x y z
% plane = dot(normal, [x, y, z]);
d = dot(plane_norm, plane_point);

for xx=1:length(sphere_x)
    for yy=1:length(sphere_y)
        plane_z = (d - a*xx - b*yy) / c;
        
        if sphere_z(xx,yy) > plane_z
%             sphere_z(xx,yy) = plane_z;
        end
    end
end

sphere_z(:,10) = sphere_z(:,10) + 1
figure
surf(sphere_x,sphere_y,sphere_z)

