import streamlit as st
import math
import sympy as sp
import numpy as np
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
        "Story Optimization"
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

    func_input = st.text_input("Enter function of x:", "x**2")
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
# PAGE 4: STORY OPTIMIZATION
# ============================
elif page == "Story Optimization":
    st.markdown("<div class='title'>Story-Based Optimization Solver</div>", unsafe_allow_html=True)

    st.info("""
    Menyelesaikan soal cerita optimasi terbatas pada:
    **Luas, Keliling, Volume, dan Keuntungan**
    """)

    category = st.selectbox(
        "Pilih jenis soal:",
        ["Luas", "Keliling", "Volume", "Keuntungan"]
    )

    x = sp.symbols('x', positive=True)

    # ===== LUAS =====
    if category == "Luas":
        P = st.number_input("Keliling persegi panjang:", value=40.0)
        y = (P / 2) - x
        A = x * y

        st.latex(f"A(x) = x({P}/2 - x)")
        critical = sp.solve(sp.diff(A, x), x)[0]

        st.success(f"""
        Luas maksimum terjadi saat:
        x = {critical}, y = {y.subs(x, critical)}
        Luas maksimum = {A.subs(x, critical)}
        """)

    # ===== KELILING =====
    elif category == "Keliling":
        L = st.number_input("Luas tetap:", value=100.0)
        y = L / x
        P = 2 * (x + y)

        st.latex("P(x) = 2(x + L/x)")
        critical = sp.solve(sp.diff(P, x), x)[0]

        st.success(f"""
        Keliling minimum terjadi saat:
        x = {critical}, y = {y.subs(x, critical)}
        Keliling minimum = {P.subs(x, critical)}
        """)

    # ===== VOLUME =====
    elif category == "Volume":
        st.warning("Contoh sederhana: kotak tanpa tutup")
        L = st.number_input("Panjang karton:", value=20.0)
        W = st.number_input("Lebar karton:", value=20.0)

        V = x * (L - 2*x) * (W - 2*x)
        critical = sp.solve(sp.diff(V, x), x)

        critical = [c for c in critical if c.is_real and c > 0]

        if critical:
            c = critical[0]
            st.latex("V(x) = x(L - 2x)(W - 2x)")
            st.success(f"""
            Volume maksimum saat x = {c}
            Volume maksimum = {V.subs(x, c)}
            """)
        else:
            st.warning("Tidak ada solusi valid.")

    # ===== KEUNTUNGAN =====
    elif category == "Keuntungan":
        harga = st.number_input("Harga per unit:", value=50.0)
        biaya = st.number_input("Biaya per unit:", value=20.0)
        biaya_tetap = st.number_input("Biaya tetap:", value=100.0)

        q = sp.symbols('q', real=True)
        profit = harga*q - (biaya*q + biaya_tetap)

        critical = sp.solve(sp.diff(profit, q), q)

        if critical:
            st.latex("P(q) = harga·q - (biaya·q + biaya tetap)")
            st.success(f"""
            Keuntungan maksimum saat:
            q = {critical[0]}
            Keuntungan maksimum = {profit.subs(q, critical[0])}
            """)
        else:
            st.warning("Tidak ada titik maksimum.")
