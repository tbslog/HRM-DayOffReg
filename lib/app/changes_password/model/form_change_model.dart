class FormChangePasswordModel {
  String? username;
  String? currentPassword;
  String? newPassword;
  String? confirmPass;

  FormChangePasswordModel(
      {this.username,
      this.currentPassword,
      this.newPassword,
      this.confirmPass});

  FormChangePasswordModel.fromJson(Map<String, dynamic> json) {
    username = json['username'];
    currentPassword = json['currentPassword'];
    newPassword = json['newPassword'];
    confirmPass = json['confirmPass'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['username'] = username;
    data['currentPassword'] = currentPassword;
    data['newPassword'] = newPassword;
    data['confirmPass'] = confirmPass;
    return data;
  }
}
