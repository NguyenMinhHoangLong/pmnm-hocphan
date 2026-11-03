from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError
 
 
class RegisterForm(FlaskForm):
    username = StringField(
        "Tên đăng nhập",
        filters=[lambda v: v.strip() if v else v],
        validators=[
            DataRequired(message="Vui lòng nhập tên đăng nhập."),
            Length(min=4, max=20, message="Tên đăng nhập phải từ 4 đến 20 ký tự."),
            Regexp(r"^[a-z0-9_]+$",
                   message="Tên đăng nhập chỉ gồm chữ thường không dấu, số và dấu gạch dưới (_)."),
        ],
    )
    email = StringField(
        "Email",
        filters=[lambda v: v.strip() if v else v],
        validators=[
            DataRequired(message="Vui lòng nhập email."),
            Regexp(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", message="Email không đúng định dạng."),
        ],
    )
    password = PasswordField(
        "Mật khẩu",
        validators=[
            DataRequired(message="Vui lòng nhập mật khẩu."),
            Length(min=8, message="Mật khẩu tối thiểu 8 ký tự."),
        ],
    )
    confirm = PasswordField(
        "Nhập lại mật khẩu",
        validators=[EqualTo("password", message="Mật khẩu nhập lại không khớp.")],
    )
    agree = BooleanField(
        "Tôi đồng ý với điều khoản sử dụng",
        validators=[DataRequired(message="Bạn phải đồng ý với điều khoản.")],
    )
 
    # Validator riêng: kiểm tra trùng tên với USERS của Bài 4 (phân biệt hoa thường)
    def validate_username(self, field):
        if field.data in current_app.config["USERS"]:
            raise ValidationError("Tên đăng nhập đã được sử dụng.")
 