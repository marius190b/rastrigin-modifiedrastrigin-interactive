import numpy as np
import plotly.graph_objects as go

# ============================================================
# Blended Rastrigin function (same logic as your MATLAB version)
# ============================================================
def blended_rastrigin(x1, x2, alpha):
    """
    alpha = 0  → Standard Rastrigin
    alpha = 1  → Modified Rastrigin
    Uses the efficient closed-form blending you derived.
    """
    return (20 - 10 * alpha) + \
           ((1 - 2 * alpha) * x1**2 + (-10 + 15 * alpha) * np.cos(2 * np.pi * x1)) + \
           ((1 - 2 * alpha) * x2**2 + (-10 + 15 * alpha) * np.cos(2 * np.pi * x2))


# ============================================================
# Create grid
# ============================================================
x = np.linspace(-5.12, 5.12, 150)
X, Y = np.meshgrid(x, x)

# Alpha values for the slider (11 steps = smooth enough)
alphas = np.linspace(0, 1, 11)

# Precompute all surfaces
frames = []
for alpha in alphas:
    Z = blended_rastrigin(X, Y, alpha)
    frame = go.Frame(
        data=[go.Surface(
            z=Z,
            x=X,
            y=Y,
            colorscale='Jet',
            showscale=True,
            colorbar=dict(title='f(x)')
        )],
        name=f"{alpha:.1f}"
    )
    frames.append(frame)

# Initial surface (alpha = 0)
Z0 = blended_rastrigin(X, Y, 0.0)
initial_surface = go.Surface(
    z=Z0,
    x=X,
    y=Y,
    colorscale='Jet',
    showscale=True,
    colorbar=dict(title='f(x)')
)

# ============================================================
# Create figure
# ============================================================
fig = go.Figure(data=[initial_surface], frames=frames)

# ============================================================
# Layout & Slider
# ============================================================
fig.update_layout(
    title=dict(
        text="Rastrigin Function Transition<br><sup>α = 0 (Standard) → α = 1 (Modified)</sup>",
        x=0.5,
        font=dict(size=20)
    ),
    scene=dict(
        xaxis_title='x₁',
        yaxis_title='x₂',
        zaxis_title='f(x)',
        aspectmode='cube',
        camera=dict(eye=dict(x=1.8, y=1.8, z=1.2)),
        zaxis=dict(range=[-45, 80])   # same limits as your MATLAB version
    ),
    width=900,
    height=750,
    margin=dict(l=0, r=0, t=80, b=0),
    
    # Slider
    sliders=[{
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "prefix": "Transition parameter α = ",
            "visible": True,
            "xanchor": "right",
            "font": {"size": 16, "color": "#000"}
        },
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": [
            {
                "args": [
                    [f"{alpha:.1f}"],
                    {
                        "frame": {"duration": 0, "redraw": True},
                        "mode": "immediate",
                        "transition": {"duration": 0}
                    }
                ],
                "label": f"{alpha:.1f}",
                "method": "animate"
            }
            for alpha in alphas
        ]
    }],
    
    # Play / Pause button
    updatemenus=[{
        "type": "buttons",
        "showactive": False,
        "y": 0.8,
        "x": 1.05,
        "xanchor": "left",
        "yanchor": "top",
        "pad": {"t": 0, "r": 10},
        "buttons": [
            {
                "label": "▶ Play",
                "method": "animate",
                "args": [None, {
                    "frame": {"duration": 400, "redraw": True},
                    "fromcurrent": True,
                    "mode": "immediate",
                    "transition": {"duration": 300}
                }]
            },
            {
                "label": "⏸ Pause",
                "method": "animate",
                "args": [[None], {
                    "frame": {"duration": 0, "redraw": False},
                    "mode": "immediate",
                    "transition": {"duration": 0}
                }]
            }
        ]
    }]
)

# ============================================================
# Export to interactive HTML (self-contained)
# ============================================================
fig.write_html(
    "Rastrigin_Transition_Interactive.html",
    include_plotlyjs=True,   # makes the file self-contained
    full_html=True,
    auto_open=True           # opens in browser automatically
)

print("✅ Exported: Rastrigin_Transition_Interactive.html")
print("   Open this file in any browser — slider and animation work offline.")