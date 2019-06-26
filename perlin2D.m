%
%
% rad = 5;
%
% phi = linspace(0, pi, 20);
% theta = linspace(0, 2 * pi, 40);
% x = outer(sin(theta), cos(phi));
% y = np.outer(np.sin(theta), np.sin(phi))
% z = np.outer(np.cos(theta), np.ones_like(phi))


function s = perlin2D(m)
s = zeros([m,m]);     % Prepare output image (size: m x m)
w = m;
i = 0;
while w > 3
    i = i + 1;
    d = interp2(randn([m,m]), i-1, 'spline');
    s = s + i * d(1:m, 1:m);
    w = w - ceil(w/2 - 1);
end
s = (s - min(min(s(:,:)))) ./ (max(max(s(:,:))) - min(min(s(:,:))));
end


