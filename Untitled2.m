r = 0:1:60;
theta = 0:pi/30:2*pi;
for i = 1:61
    r(i) = i-1;
    if (r(i) < 3)
        sigmar(i) = -6;
    else
        sigmar(i) = ((1-((7^2)/(r(i)^2)))*-14);   %multiplier is a predefined constant
    end
end
[x,y] = pol2cart(theta, r);
[X,Y] = meshgrid(x,y);
sigmar = repmat(sigmar,61,1);
surf(X,Y,sigmar)