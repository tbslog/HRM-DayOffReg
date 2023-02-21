class Validate {
  String username(String? value) {
    if (value!.isEmpty) {
      return "Nhập tài khoản";
    } else {
      return "";
    }
  }

  String password(String? value) {
    if (value!.isEmpty) {
      return "Nhập mật khẩu";
    } else {
      return "";
    }
  }

  String rePassword(String? value) {
    if (value!.isEmpty) {
      return "Nhập lại mật khẩu";
    } else {
      return "";
    }
  }
}
