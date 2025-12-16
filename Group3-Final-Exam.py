import streamlit as st
import math
import sympy as sp
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Safe for deployment
import matplotlib.pyplot as plt
import base64

# ============================
# PAGE CONFIG
# ============================
st.set_page_config(
    page_title="Math Web App",
    page_icon="🧮",
    layout="wide"
)

# ============================
# FUNCTION: IMAGE TO BASE64
# ============================
def img_to_base64(filepath):
    try:
        with open(filepath, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

# ============================
# CSS STYLING
# ============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"] {
    background: transparent !important;
}
html, body {
    background: linear-gradient(140deg, #002060, #C00000);
}
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: black;
    margin-bottom: 30px;
    text-shadow: 2px 2px 6px rgba(255,255,255,0.4);
}
.member-card {
    background: linear-gradient(135deg, #002060, #C00000);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    text-align: center;
    border: 3px solid white;
    width: 280px;
    height: 380px;
    margin: auto;
    color: white;
    transition: transform 0.3s, box-shadow 0.3s;
}
.member-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 8px 20px rgba(255,215,0,0.6);
}
.member-photo {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    border: 3px solid white;
    margin-bottom: 15px;
}
.member-name {
    font-size: 22px;
    font-weight: bold;
    color: #FFD700;
}
.member-role {
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ============================
# SIDEBAR NAVIGATION
# ============================
page = st.sidebar.radio(
    "Navigate",
    [
        "Group Members",
        "Function Tools",
        "Optimization Solver",
        "Story-Based Calculation"
    ]
)

# ============================
# PAGE 1: GROUP MEMBERS
# ============================
if page == "Group Members":
    st.markdown("<div class='title'>Group Members</div>", unsafe_allow_html=True)

    members = [
        {"name": "Pardi Ihsan", "role": "Leader / Project Execution", "photo": "Pardi.jpeg"},
        {"name": "Fikri Ariansyah", "role": "Member / Project Execution", "photo": "Fikri.jpeg"},
        {"name": "Muhammad Adam Asyrofi", "role": "Member / Project Execution", "photo": "Adam.jpeg"},
        {"name": "Riska Dwi Ambarwati", "role": "Member / Project Execution", "photo": "Riska.jpeg"},
    ]

    cols = st.columns(2)
    for i, m in enumerate(members):
        with cols[i % 2]:
            img64 = img_to_base64(m["photo"])
            st.markdown(f"""
            <div class='member-card'>
                <img src="data:image/jpeg;base64,{img64}" class="member-photo">
                <div class='member-name'>{m["name"]}</div>
                <div class='member-role'>{m["role"]}</div>
            </div>
            """, unsafe_allow_html=True)

# ============================
# PAGE 2: FUNCTION TOOLS
# ============================
elif page == "Function Tools":
    st.markdown("<div class='title'>Function Visualization & Differentiation</div>", unsafe_allow_html=True)

    func_input = st.text_input("Enter a function of x:", "x**2")
    x = sp.symbols('x')

    try:
        expr = sp.sympify(func_input)
        f = sp.lambdify(x, expr, "numpy")
        x_vals = np.linspace(-10, 10, 400)
        y_vals = f(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        st.pyplot(fig)

        derivative = sp.diff(expr, x)
        st.success(f"Derivative: {derivative}")

    except:
        st.error("Invalid function input.")

# ============================
# PAGE 3: OPTIMIZATION SOLVER
# ============================
elif page == "Optimization Solver":
    st.markdown("<div class='title'>Optimization Solver</div>", unsafe_allow_html=True)

    var_input = st.text_input("Variable(s):", "x")
    func_input = st.text_input("Function:", "-x**2 + 4*x")
    opt_type = st.radio("Optimization Type:", ["Maximize", "Minimize"])

    try:
        vars_list = [sp.symbols(v.strip()) for v in var_input.split(",")]
        func = sp.sympify(func_input)

        derivs = [sp.diff(func, v) for v in vars_list]
        crit_points = sp.solve(derivs, vars_list, dict=True)

        if crit_points:
            best = max(crit_points, key=lambda p: func.subs(p)) if opt_type == "Maximize" \
                   else min(crit_points, key=lambda p: func.subs(p))
            st.success(f"{opt_type} at {best} with value {func.subs(best)}")
        else:
            st.warning("No critical points found.")

    except Exception as e:
        st.error(e)

# ============================
# PAGE 4: STORY-BASED CALCULATION
# ============================
elif page == "Story-Based Calculation":
    st.markdown("<div class='title'>Story-Based Calculation</div>", unsafe_allow_html=True)
    st.info("Enter numbers according to the word problem, choose the shape:")

    category = st.selectbox(
        "Select category:",
        ["Area", "Perimeter", "Volume", "Profit"]
    )

    if category == "Area":
        st.subheader("Area")
        shape = st.selectbox("Select shape:", ["Rectangle", "Triangle", "Trapezoid", "Circle"])

        if shape == "Rectangle":
            length = st.number_input("Enter length:", value=10.0)
            width = st.number_input("Enter width:", value=5.0)
            area = length * width
            st.success(f"Area = {length} × {width} = {area}")

        elif shape == "Triangle":
            base = st.number_input("Enter base:", value=8.0)
            height = st.number_input("Enter height:", value=5.0)
            area = 0.5 * base * height
            st.success(f"Area = 0.5 × {base} × {height} = {area}")

        elif shape == "Trapezoid":
            a = st.number_input("Enter parallel side a:", value=8.0)
            b = st.number_input("Enter parallel side b:", value=5.0)
            height = st.number_input("Enter height:", value=4.0)
            area = 0.5 * (a + b) * height
            st.success(f"Area = 0.5 × ({a} + {b}) × {height} = {area}")

        elif shape == "Circle":
            r = st.number_input("Enter radius:", value=7.0)
            area = math.pi * r**2
            st.success(f"Area = π × {r}² = {area:.2f}")

    elif category == "Perimeter":
        st.subheader("Perimeter")
        shape = st.selectbox("Select shape:", ["Rectangle", "Triangle", "Trapezoid", "Circle"])

        if shape == "Rectangle":
            length = st.number_input("Enter length:", value=10.0)
            width = st.number_input("Enter width:", value=5.0)
            perimeter = 2 * (length + width)
            st.success(f"Perimeter = 2 × ({length} + {width}) = {perimeter}")

        elif shape == "Triangle":
            a = st.number_input("Side a:", value=5.0)
            b = st.number_input("Side b:", value=6.0)
            c = st.number_input("Side c:", value=7.0)
            perimeter = a + b + c
            st.success(f"Perimeter = {a} + {b} + {c} = {perimeter}")

        elif shape == "Trapezoid":
            a = st.number_input("Side a:", value=8.0)
            b = st.number_input("Side b:", value=5.0)
            c = st.number_input("Side c:", value=4.0)
            d = st.number_input("Side d:", value=3.0)
            perimeter = a + b + c + d
            st.success(f"Perimeter = {a} + {b} + {c} + {d} = {perimeter}")

        elif shape == "Circle":
            r = st.number_input("Enter radius:", value=7.0)
            perimeter = 2 * math.pi * r
            st.success(f"Perimeter = 2 × π × {r} = {perimeter:.2f}")

    elif category == "Volume":
        st.subheader("Volume")
        shape = st.selectbox("Select shape:", ["Cuboid", "Cylinder", "Triangular Prism", "Triangular Pyramid"])

        if shape == "Cuboid":
            length = st.number_input("Length:", value=10.0)
            width = st.number_input("Width:", value=5.0)
            height = st.number_input("Height:", value=4.0)
            volume = length * width * height
            st.success(f"Volume = {length} × {width} × {height} = {volume}")

        elif shape == "Cylinder":
            r = st.number_input("Radius:", value=7.0)
            height = st.number_input("Height:", value=10.0)
            volume = math.pi * r**2 * height
            st.success(f"Volume = π × {r}² × {height} = {volume:.2f}")

        elif shape == "Triangular Prism":
            base = st.number_input("Triangle base:", value=6.0)
            height_triangle = st.number_input("Triangle height:", value=4.0)
            length = st.number_input("Prism length:", value=10.0)
            volume = 0.5 * base * height_triangle * length
            st.success(f"Volume = 0.5 × {base} × {height_triangle} × {length} = {volume}")

        elif shape == "Triangular Pyramid":
            base = st.number_input("Triangle base:", value=6.0)
            height_triangle = st.number_input("Triangle height:", value=4.0)
            height_pyramid = st.number_input("Pyramid height:", value=10.0)
            volume = (1/3) * 0.5 * base * height_triangle * height_pyramid
            st.success(f"Volume = 1/3 × 0.5 × {base} × {height_triangle} × {height_pyramid} = {volume}")

    elif category == "Profit":
        st.subheader("Profit")
        price = st.number_input("Price per unit:", value=50.0)
        cost = st.number_input("Cost per unit:", value=20.0)
        fixed_cost = st.number_input("Fixed cost:", value=100.0)

        q = sp.symbols('q', real=True)
        profit = price*q - (cost*q + fixed_cost)

        critical = sp.solve(sp.diff(profit, q), q)

        st.latex("P(q) = price·q - (cost·q + fixed cost)")
        if critical:
            st.success(f"""
            Maximum profit occurs at:
            q = {critical[0]}
            Maximum profit = {profit.subs(q, critical[0])}
            """)
        else:
            st.warning("No maximum point (linear function)")
