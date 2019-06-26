sphereSource = sphere;


rad = 5;
size = 32;
phi = linspace(0, pi, size);
theta = linspace(0, 2 * pi, size);
% x = outer(sin(theta), cos(phi));
% y = np.outer(np.sin(theta), np.sin(phi))
% z = np.outer(np.cos(theta), np.ones_like(phi))
[x ,y] = pol2cart(theta, phi);


% perlin noise:
s = zeros([size, size]);
w = m;
i = 0;
while w > 3
    i = i + 1;
    d = interp2(randn([size,size]), i-1, 'spline');
    s = s + i * d(1:size, 1:size);
    w = w - ceil(w/2 - 1);
end
s = (s - min(min(s(:,:)))) ./ (max(max(s(:,:))) - min(min(s(:,:))));

% [theta,rho,z] = cart2pol(x, y, s);
% surf(theta, rho, z)
% surf(s)





   
   
   