```markdown
# 🏗️ Crane Motor Telemetry: Advanced Diagnostics App

An ultra-modern, interactive [Streamlit](https://streamlit.io/) application designed to simulate and analyze crane motor performance. This tool features a gamified, multi-stage learning environment where users must mathematically derive and input system constraints to unlock real-time load line intersection telemetry.

Designed with a sleek "Deep Dark Mode" UI, glass-morphism cards, and neon accents, it brings industrial motor diagnostics to life.

---

## 📑 Table of Contents
1. [Features](#features)
2. [Prerequisites & Installation](#prerequisites--installation)
3. [Usage Guide](#usage-guide)
4. [Code Architecture](#code-architecture)
5. [How to Modify the Code](#how-to-modify-the-code)
6. [Deployment to Streamlit Cloud](#deployment-to-streamlit-cloud)

---

## ✨ Features
* **Multi-Stage Validation System:** The visualization canvas remains "Offline" until the user correctly computes starting torques, selects the correct motor, and derives the algebraic constants.
* **Live LaTeX Rendering:** As users input their derived structural constants ($A$, $B$, $C$, $D$), the mathematical equations update in real-time.
* **Advanced Telemetry Visualization:** Utilizes `plotly.graph_objects` to plot motor torque-speed curves against an ideal exponential load line.
* **Algorithmic Intersection Finding:** Leverages `scipy.optimize.fsolve` to dynamically calculate and annotate the exact operational intersection points on the graph.
* **Ultra-Modern UI/UX:** Custom CSS injection overrides default Streamlit styling to provide a highly polished, interactive dashboard experience.

---

## 🛠️ Prerequisites & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/crane-motor-telemetry.git](https://github.com/yourusername/crane-motor-telemetry.git)
cd crane-motor-telemetry

```

### 2. Install Dependencies

Ensure you have Python 3.8+ installed. This app relies on numerical processing and graphing libraries. Install them via pip:

```bash
pip install streamlit numpy plotly scipy

```

*(Recommended: Create a `requirements.txt` file in your repository with the following contents:)*

```text
streamlit
numpy
plotly
scipy

```

### 3. Run the Application

```bash
streamlit run app.py

```

*Note: Replace `app.py` with the actual name of your Python script.*

---

## 🚀 Usage Guide

1. **Review Operational Goals:** Check the top-left glass cards for the required system constraints (e.g., maximum current limit of 80 A).
2. **Phase 1 (Sections 1-3):** * Calculate the starting torque for Motor 1 and Motor 2.
* Select the appropriate motor for the crane application.
* Input the derived mathematical constants ($A, B, C, D$) to define the motor speed equations.


3. **Initialize Telemetry:** Click the primary button. If your math is strictly correct, the system unlocks the plotting canvas. If incorrect, the app provides diagnostic hints.
4. **Phase 2 (Section 4):** Once the plot renders, read the dynamic intersection coordinates on the graph to answer the final profiling questions at specific loads (48 Nm and 12 Nm). Click **Verify Operational Speeds** to complete the diagnostics.

---

## 🏗️ Code Architecture

The application is structured into a highly stylized **2-Column Layout (Left: 1 | Right: 1.6)** to separate data entry from visualization.

* **UI/UX Injection:** A large HTML/CSS block at the top overrides Streamlit's default components, applying custom fonts (Inter), dark themes, gradient texts, and hover effects.
* **State Management (`st.session_state`):** Tracks the `plot_unlocked` boolean. This ensures the graph and the final set of questions only appear *after* Phase 1 is validated.
* **Left Column:**
* Information Cards (Operational Goals & Specs).
* Input fields for Torques, Motor Selection, and Algebraic Constants.
* Live Equation preview box.


* **Right Column:**
* **Validation Engine:** Checks user inputs against hardcoded correct values with specific mathematical tolerances.
* **Intersection Logic:** A custom `find_intersections()` function uses SciPy's `fsolve` to mathematically locate where the motor curves cross the load curve.
* **Plotly Canvas:** Renders the dynamic chart and text annotations based on the found roots.
* **Final Verification:** Section 4 load profiling (unlocked dynamically).



---

## 🔧 How to Modify the Code

### 1. Changing the Correct Answers

To change the mathematical requirements for unlocking the plot, update the `correct_` variables located at the top of the **Right Column** logic:

```python
correct_t1, correct_t2 = 120.0, 192.0
correct_a, correct_b = 160.0, 0.1778
correct_c, correct_d = 240.0, 13.33

```

### 2. Modifying the Curves & Physics Logic

To change how the actual lines are drawn (and where they intersect), modify the Python functions inside the `if st.session_state.plot_unlocked:` block:

```python
# Change the underlying math for the ideal load
def load_curve(T): return 516.45 * np.exp(-0.01829 * T) - 27.69

# Change how the app calculates the motor curves based on user input
def motor1_curve(T): return blank_a - blank_b * T

```

### 3. Adjusting Tolerances

Because floating-point math can be imprecise, the app uses tolerances to check user inputs. You can tighten or loosen these bounds:

```python
# Change 0.001 to a larger number to make grading more forgiving
eq1_correct = (blank_a == correct_a) and (abs(blank_b - correct_b) < 0.001)

```

### 4. Customizing UI Colors

Locate the CSS block at the top of the script. You can easily swap out hex codes to change the theme.

* Primary Cyan: `#00C9FF`
* Emerald Accent: `#34D399`
* Background Dark: `#0B0F19`

---

## ☁️ Deployment to Streamlit Cloud

Deploying this app to the public web is free and straightforward using Streamlit Community Cloud.

1. **Push to GitHub:** Ensure your `app.py` and `requirements.txt` (crucial for `scipy`) are pushed to your GitHub repository.
2. **Log into Streamlit Cloud:** Visit [share.streamlit.io](https://share.streamlit.io/) and connect your GitHub account.
3. **Deploy the App:**
* Click **"New app"**.
* Select your repository, the branch (e.g., `main`), and the main file path (`app.py`).
* Click **"Deploy!"**


4. **Wait for Build:** Streamlit will automatically read your `requirements.txt` and install `numpy`, `plotly`, and `scipy`. Once finished, you will receive a public, shareable URL.

```

```
