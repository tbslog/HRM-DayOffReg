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
      if (value.length <= 6 && value.length >= 10) {
        return "Mật khẩu tối thiểu 6 kí tự và tối đa 10 kí tự";
      }
      return "";
    }
  }

  String rePassword(String? value1, String value2) {
    if (value1!.isEmpty) {
      return "Nhập lại mật khẩu";
    } else {
      if (value1.length <= 6 && value1.length >= 10) {
        return "Mật khẩu tối thiểu 6 kí tự và tối đa 10 kí tự";
      } else {
        if (value1 != value2) {
          return "Mật khẩu không trùng khớp";
        }
        return "";
      }
    }
  }
}
