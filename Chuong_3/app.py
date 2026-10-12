from flask import Flask, request, abort, redirect, Response
from markupsafe import escape
import csv 
import io
app = Flask(__name__)
STUDENTS = {
    "23T1020001": {"name": "Nguyễn Văn An", "Lop": "K47A", "scores": {"PMNM": 8.5, "CSDL": 7.0, "MMT": 9.0}},
    "23T1020002": {"name": "Trần Thị Bình", "Lop": "K47A", "scores": {"PMNM": 6.0, "CSDL": 5.5, "MMT": 7.0}},
    "23T1020003": {"name": "Lê Hoàng Cường", "Lop": "K47B", "scores": {"PMNM": 9.5, "CSDL": 9.0}},
    "23T1020004": {"name": "Phạm Minh Dũng", "Lop": "K47B", "scores": {"PMNM": 4.0, "CSDL": 3.5, "MMT": 5.0}},
    "23T1020005": {"name": "Hoàng Thu Hà", "Lop": "K47A", "scores": {}},
    "23T1020006": {"name": "Võ Quốc Khánh", "Lop": "K47C", "scores": {"PMNM": 7.5, "MMT": 9.0}}
}

@app.route("/")
def home():
    total_students = len(STUDENTS)
    classes = set(student["Lop"] for student in STUDENTS.values())
    total_classes = len(classes)
    return f"""
    <h1>Quản lý sinh viên </h1>
    <p>Tổng số sinh viên: {total_students}</p>
    <p>Số lớp: {total_classes}</p>
    <a href="/students">Danh sách sinh viên</a>
    <br>
    <a href="/api/students">API sinh viên</a>
    """



@app.route("/students")
def students():
    lop_loc = request.args.get("lop","").strip().lower()
    classes = sorted(set(student["Lop"] for student in STUDENTS.values()))
    loc_sinhvien = []
    for mssv, student in STUDENTS.items():
        if lop_loc == "" or student["Lop"].lower() == lop_loc:
            loc_sinhvien.append((mssv,student))
    # tạo bảng
    html = """
    <h1>Danh sách sinh viên</h1>
    <p>
        <a href="/students">Tất cả</a>
    </p>
    """
    # lọc lớp từ dữ liệu
    for lop in classes:
        html += f' | <a href="/students?lop={lop}">{lop}</a>'
    html += "</p>"
    if not loc_sinhvien:
        html += "<p>Không có sinh viên phù hợp</p>"
        return html
    html += """
    <table border="1" cellpadding="8">
        <tr>
            <th>MSSV</th>
            <th>Họ tên</th>
            <th>Lớp</th>
            <th>Điểm TB</th>
            <th>Xếp loại</th>
        </tr>
    """
    for mssv, student in loc_sinhvien:
        scores = student["scores"]
        if len(scores) == 0:
            avg = None
            rank = "-"
        else:
            avg = sum(scores.values()) / len(scores)
            if avg>=8:
                rank = "Giỏi"
            elif avg>=6.5:
                rank = "Khá"
            elif avg>=5:
                rank = "Trung bình"
            else:
                rank = "Yếu"
        avg_display = " - " if avg is None else f"{avg:.2f}" 
        html += f"""
        <tr>
            <td><a href="/students/{mssv}">{mssv}</a></td>
            <td>{student["name"]}</td>
            <td>{student["Lop"]}</td>
            <td>{avg_display}</td>
            <td>{rank}</td>
        </tr>
        """
    html += "</table>"
    return html
# câu 3
@app.route("/students/<mssv>")
def thongtin_sinhvien(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
    student = STUDENTS[mssv]
    name = student["name"]
    lop = student["Lop"]
    scores = student["scores"]

    if len(scores) == 0 :
        avg = None
        rank = "-"
    else:
        avg = sum(scores.values()) / len(scores)

        if avg >= 8:
            rank = "Giỏi"
        elif avg >= 6.5:
            rank = "Khá"
        elif avg >= 5:
            rank = "Trung bình"
        else:
            rank = "Yếu"

    avg_display = "-" if avg is None else f"{avg:.2f}"

    html = f"""
    <h1>Thông tin sinh viên</h1>

    <p><b>Họ tên:</b> {name}</p>
    <p><b>MSSV:</b> {mssv}</p>
    <p>
        <b>Lớp:</b>
        <a href="/students?lop={lop}">{lop}</a>
    </p>
    <p><b>Điểm TB:</b> {avg_display}</p>
    <p><b>Xếp loại:</b> {rank}</p>

    <h2>Bảng điểm</h2>

    <table border="1" cellpadding="8">
        <tr>
            <th>Học phần</th>
            <th>Điểm</th>
        </tr>
    """
    for hoc_phan, diem in scores.items():
        html += f"""
        <tr>
            <td>{hoc_phan}</td>
            <td>{diem}</td>
        </tr>
        """

    html += f"""
    </table>
    <br>
    <a href="/students/{mssv}/export">
        Tải bảng điểm (CSV)
    </a>

    <br>
    <a href="/sv/{mssv}">
        Liên kết rút gọn
    </a>

    <br>
    <a href="/students">Quay lại danh sách sinh viên</a>
    """
    return html
# câu 4
@app.route("/sv/<mssv>")
def old_student_url(mssv):
    return redirect(f"/students/{mssv}", code=301)

# câu 5
@app.route("/students/<mssv>/export")
def export_scores(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")

    student = STUDENTS[mssv]
    scores = student["scores"]

    output = io.StringIO(newline="")
    writer = csv.writer(output)

    # Ghi tiêu đề cột
    writer.writerow(["hoc_phan", "diem"])

    # Ghi điểm từng học phần
    for hoc_phan, diem in scores.items():
        writer.writerow([hoc_phan, diem])

    # Tạo phản hồi để trình duyệt tải file
    response = Response(
        "\ufeff" + output.getvalue(),
        content_type="text/csv; charset=utf-8"
    )

    response.headers["Content-Disposition"] = (
        f'attachment; filename="bang_diem_{mssv}.csv"'
    )
    return response
# câu 6
@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    safe_q = escape(query)  # Escape an toàn chống XSS

    results = []
    if query:
        q_lower = query.lower()
        for mssv, student in STUDENTS.items():
            # Tìm theo họ tên (không phân biệt hoa thường) hoặc MSSV chứa từ khoá
            if q_lower in student["name"].lower() or q_lower in mssv.lower():
                results.append((mssv, student))

    html = f"""
    <h1>Tìm kiếm sinh viên</h1>
    <form method="GET" action="/search">
        <input type="text" name="q" value="{safe_q}" placeholder="Nhập tên hoặc MSSV...">
        <button type="submit">Tìm</button>
    </form>
    """

    if query:
        html += f'<p>Tìm thấy {len(results)} kết quả cho "{safe_q}":</p>'
        if results:
            html += "<ul>"
            for mssv, student in results:
                html += f'<li><a href="/students/{mssv}">{student["name"]} ({mssv})</a> - Lớp {student["Lop"]}</li>'
            html += "</ul>"
        else:
            html += "<p>Không tìm thấy sinh viên nào.</p>"

    html += '<br><a href="/students">Quay lại danh sách</a>'
    return html
if __name__ == "__main__": 
    app.run(debug=True)
