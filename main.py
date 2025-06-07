import numpy as np
import plotly.graph_objects as go

def create_cube(center, size, color):
    c = np.array(center)
    s = size / 2
    vertices = np.array([
        c + [-s, -s, -s], c + [ s, -s, -s], c + [ s,  s, -s], c + [-s,  s, -s],
        c + [-s, -s,  s], c + [ s, -s,  s], c + [ s,  s,  s], c + [-s,  s,  s],
    ])
    faces = [
        [0,1,2], [0,2,3],
        [4,5,6], [4,6,7],
        [0,1,5], [0,5,4],
        [2,3,7], [2,7,6],
        [1,2,6], [1,6,5],
        [3,0,4], [3,4,7],
    ]
    I, J, K = zip(*faces)
    return go.Mesh3d(
        x=vertices[:,0], y=vertices[:,1], z=vertices[:,2],
        i=I, j=J, k=K,
        color=color, opacity=1.0, flatshading=False,
        lighting=dict(ambient=0.5, diffuse=0.9, roughness=0.4, specular=0.4),
        lightposition=dict(x=100, y=200, z=0)
    )

def create_cylinder(center, radius, height, color, resolution=50):
    x0, y0, z0 = center
    theta = np.linspace(0, 2*np.pi, resolution)
    x_circle = radius * np.cos(theta)
    y_circle = radius * np.sin(theta)
    x = np.concatenate([x0 + x_circle, x0 + x_circle])
    y = np.concatenate([y0 + y_circle, y0 + y_circle])
    z = np.concatenate([np.full(resolution, z0), np.full(resolution, z0 + height)])

    I, J, K = [], [], []
    for i in range(resolution):
        next_i = (i + 1) % resolution
        I += [i, next_i, i + resolution]
        J += [next_i, next_i + resolution, i + resolution]
        K += [next_i + resolution, next_i, i]

    x = np.append(x, [x0, x0])
    y = np.append(y, [y0, y0])
    z = np.append(z, [z0, z0 + height])
    center_bottom = 2 * resolution
    center_top = 2 * resolution + 1

    for i in range(resolution):
        next_i = (i + 1) % resolution
        I += [center_bottom]
        J += [i]
        K += [next_i]
        I += [center_top]
        J += [i + resolution]
        K += [next_i + resolution]

    return go.Mesh3d(
        x=x, y=y, z=z, i=I, j=J, k=K,
        color=color, opacity=1.0, flatshading=False,
        lighting=dict(ambient=0.5, diffuse=0.9, roughness=0.4, specular=0.3),
        lightposition=dict(x=100, y=200, z=0)
    )

def create_sphere(center, radius, color, resolution=40):
    u = np.linspace(0, 2*np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
    y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]

    x = x.flatten()
    y = y.flatten()
    z = z.flatten()

    I, J, K = [], [], []
    for i in range(resolution - 1):
        for j in range(resolution - 1):
            p1 = i * resolution + j
            p2 = p1 + 1
            p3 = p1 + resolution
            p4 = p3 + 1
            I += [p1, p2, p1]
            J += [p3, p3, p2]
            K += [p4, p4, p4]

    return go.Mesh3d(
        x=x, y=y, z=z, i=I, j=J, k=K,
        color=color, opacity=1.0, flatshading=False,
        lighting=dict(ambient=0.4, diffuse=0.9, roughness=0.4, specular=0.5),
        lightposition=dict(x=100, y=200, z=0)
    )

def create_cone(center, radius, height, color, resolution=50):
    x0, y0, z0 = center
    theta = np.linspace(0, 2*np.pi, resolution)
    x_circle = radius * np.cos(theta)
    y_circle = radius * np.sin(theta)
    x = np.append(x0 + x_circle, x0)
    y = np.append(y0 + y_circle, y0)
    z = np.append(np.full(resolution, z0), z0 + height)
    apex = resolution

    I, J, K = [], [], []
    for i in range(resolution):
        next_i = (i + 1) % resolution
        I += [i, apex, apex]
        J += [next_i, i, next_i]
        K += [apex, next_i, i]

    return go.Mesh3d(
        x=x, y=y, z=z, i=I, j=J, k=K,
        color=color, opacity=1.0, flatshading=False,
        lighting=dict(ambient=0.5, diffuse=0.9, roughness=0.3, specular=0.7),
        lightposition=dict(x=100, y=200, z=0)
    )

def build_robot_and_show():
    fig = go.Figure()

    # Badan (kubus)
    fig.add_trace(create_cube(center=[0, 0, 0], size=3.0, color='lightblue'))
    # Leher (silinder)
    fig.add_trace(create_cylinder(center=[0, 0, 1.5], radius=0.35, height=1.5, color='red'))
    # Kepala (kubus kecil)
    fig.add_trace(create_cube(center=[0, 0, 3.0], size=1.5, color='deepskyblue'))
    # Mata kiri (bola)
    fig.add_trace(create_sphere(center=[-0.4, 0.75, 3.0], radius=0.3, color='white'))
    # Mata kanan (bola)
    fig.add_trace(create_sphere(center=[0.4, 0.75, 3.0], radius=0.3, color='white'))
    # Tangan kiri (kubus kecil)
    fig.add_trace(create_cube(center=[-1.65, 0, 0.0], size=1.2, color='dodgerblue'))
    # Tangan kanan (kubus kecil)
    fig.add_trace(create_cube(center=[1.65, 0, 0.0], size=1.2, color='dodgerblue'))
    # Antena (kerucut)
    fig.add_trace(create_cone(center=[0, 0, 3.75], radius=0.2, height=0.6, color='royalblue'))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
            bgcolor='white',
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
    )
    fig.show()

if __name__ == "__main__":
    # Untuk debug di python biasa: cetak JSON data saja
    import json
    fig = build_robot_and_show()  # ini akan menampilkan di browser via pyodide, di python biasa tidak berfungsi
