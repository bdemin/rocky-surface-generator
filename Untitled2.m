

rad = 5;

phi = linspace(0, pi, 20);
theta = linspace(0, 2 * pi, 40);
x = outer(sin(theta), cos(phi));
y = np.outer(np.sin(theta), np.sin(phi))
z = np.outer(np.cos(theta), np.ones_like(phi))