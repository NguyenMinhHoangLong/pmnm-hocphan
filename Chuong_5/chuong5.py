from datetime import date, timedelta
from functools import wraps
from forms import RegisterForm
from flask import Flask, render_template,request, flash,redirect,session,url_for
app = Flask(__name__)

# câu 1
@app.route("/", methods=["GET", "POST"])
def calc():
    values, error = {"a" : "", "b": "", "op": ""}, {}
    kq = ""

    if request.method == "POST":
        values ["a"] = request.form.get("a", "").strip()
        values ["b"] = request.form.get("b", "").strip()
        values ["op"] = request.form.get("op", "").strip()
        a = None
        b = None
        try:
            a= float(values["a"])
        except ValueError:
            error["a"] = "hãy nhập số a"

        try:
            b= float(values["b"])
        except ValueError:
            error["b"] = "hãy nhập số b"

        if values["op"] == "+":
            kq = a + b
        elif values["op"] == "-":
            kq = a - b
        elif values["op"] == "*":
            kq = a * b
        elif values["op"] == "/":
            if b==0:
                error["b"] = "Không thể chia cho 0"
            else:
                kq = a / b
        else: 
            error["op"] = "Phép toán không hợp lệ"
    return render_template("calc.html", values = values, error = error, kq = kq)



# câu 2
@app.route("/tinhdiem", methods =["GET", "POST"])
def tinhdiem():
    values, error = {"CC" : "", "GK" : "", "CK" : ""}, {}
    tongket = ""
    if request.method == "POST":
        values["CC"] = request.form.get("CC", "").strip()
        values["GK"] = request.form.get("GK", "").strip()
        values["CK"] = request.form.get("CK", "").strip()
        CC = None
        GK = None
        CK = None
        try:
            CC= float(values["CC"])
        except ValueError:
            error["CC"] = "Vui lòng nhập một số"
        try:
            GK= float(values["GK"])
        except ValueError:
            error["GK"] = "Vui lòng nhập một số"
        try:
            CK= float(values["CK"])
        except ValueError:
            error["CK"] = "Vui lòng nhập một số"
        if 0 <= CC <= 10:
            if 0 <= GK <= 10:
                if 0 <= CK <= 10:
                    tongket = CC*0.1 + GK*0.3 + CK*0.6
                else:
                    print("Điểm CK phải từ 0 đến 10")
            else:
                print("Điểm GK phải từ 0 đến 10")
        else:
            print("Điểm CC phải từ 0 đến 10")
    return render_template("tinhdiem.html",values=values,error=error,tongket=tongket)

# câu 3
def parse_float(val_str):
    if not val_str:
        return None
    # Hỗ trợ dấu phẩy thành dấu chấm thập phân (ví dụ 65,5 -> 65.5)
    val_str = val_str.strip().replace(",", ".")
    try:
        return float(val_str)
    except ValueError:
        return False  # Giá trị không phải số


@app.route("/bmi", methods=["GET", "POST"])
def calculate_bmi():
    height_raw = ""
    weight_raw = ""
    errors = {}
    result = None

    if request.method == "POST":
        height_raw = request.form.get("height", "").strip()
        weight_raw = request.form.get("weight", "").strip()

        h_val = parse_float(height_raw)
        w_val = parse_float(weight_raw)

        # Validate Chiều cao (cm)
        if h_val is None:
            errors["height"] = "Vui lòng nhập chiều cao."
        elif h_val is False:
            errors["height"] = "Vui lòng nhập một số."
        elif h_val < 50 or h_val > 250:
            msg = "Giá trị phải từ 50 đến 250."
            if h_val <= 2.5:
                msg += " (nhập mét thay vì cm)"
            errors["height"] = msg

        # Validate Cân nặng (kg)
        if w_val is None:
            errors["weight"] = "Vui lòng nhập cân nặng."
        elif w_val is False:
            errors["weight"] = "Vui lòng nhập một số."
        elif w_val < 10 or w_val > 300:
            errors["weight"] = "Giá trị phải từ 10 đến 300."

        # Nếu không có lỗi thì tiến hành tính toán
        if not errors:
            h_m = h_val / 100.0  # Đổi sang mét
            bmi = round(w_val / (h_m**2), 1)

            # Phân loại theo chuẩn Châu Á và gán màu
            if bmi < 18.5:
                category = "Thiếu cân"
                color_class = "warning"  # Vàng
            elif bmi < 23:
                category = "Bình thường"
                color_class = "success"  # Xanh
            elif bmi < 25:
                category = "Thừa cân"
                color_class = "warning"  # Vàng
            else:
                category = "Béo phì"
                color_class = "danger"  # Đỏ

            # Cân nặng nên có (BMI 18.5 - 22.9)
            w_min = round(18.5 * (h_m**2), 1)
            w_max = round(22.9 * (h_m**2), 1)

            result = {
                "bmi": bmi,
                "category": category,
                "color_class": color_class,
                "weight_range": f"{w_min} – {w_max} kg",
            }

    return render_template(
        "bmi.html",
        height=height_raw,
        weight=weight_raw,
        errors=errors,
        result=result,
    )
@app.route("/about")
def about():
    return render_template("aboutC5.html")

# buổi 2 
# câu 4
app.secret_key = "chuong5_key_bao_mat"
app.permanent_session_lifetime = timedelta(days=7)
USERS = {"admin": "admin123",
         "an": "an123456"}
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Vui lòng đăng nhập để tiếp tục.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function
@app.route("/login", methods =["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("profile"))
    username = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember")
        if username in USERS and USERS[username] == password:
            session["user"] = username
            session.permanent = True if remember else False
            flash(f"Đăng nhập thành công. Xin chào {username}!", "success")
            return redirect(url_for("profile"))
        else:
            flash("Sai tên đăng nhập hoặc mật khẩu.", "danger")
    return render_template("login.html", username = username)
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    flash("Bạn đã đăng xuất.", "info")
    return redirect(url_for("login"))
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=session["user"])
# câu 5
@app.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        return redirect(url_for("profile"))
    form = RegisterForm()
    if form.validate_on_submit():
        USERS[form.username.data] = form.password.data
        flash("Đăng ký thành công.", "success")
        return redirect(url_for("login"))
    if form.csrf_token.errors:
        flash("Phiên làm việc đã hết hạn, vui lòng thử lại.", "warning")
    return render_template("register.html", form=form)
if __name__ == "__main__":
    app.run(debug=True)
