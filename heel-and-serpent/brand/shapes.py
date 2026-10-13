"""Heel & Serpent shared palette and geometry helpers (bezier sampling, tapered ribbons)."""
import math

IRON, BONE, EMBER, ASH = "#1A1A1A", "#ECE6DA", "#C8501E", "#8A8580"


def bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / n
        a = (1-t)**3; b = 3*(1-t)**2*t; c = 3*(1-t)*t*t; d = t**3
        out.append((a*p0[0]+b*p1[0]+c*p2[0]+d*p3[0], a*p0[1]+b*p1[1]+c*p2[1]+d*p3[1]))
    return out


def ribbon(pts, w0, w1, ease=0.9):
    n = len(pts); left, right = [], []
    for i, (x, y) in enumerate(pts):
        xa, ya = pts[max(i-1, 0)]; xb, yb = pts[min(i+1, n-1)]
        dx, dy = xb-xa, yb-ya; L = math.hypot(dx, dy) or 1
        nx, ny = -dy/L, dx/L
        w = (w0 + (w1-w0) * ((i/(n-1)) ** ease)) / 2
        left.append((x+nx*w, y+ny*w)); right.append((x-nx*w, y-ny*w))
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in left + right[::-1]) + " Z"
