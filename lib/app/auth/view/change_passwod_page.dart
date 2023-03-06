import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/auth/controller/change_password_controller.dart';
import 'package:tbs_logistics_phieunghi/app/auth/moduels/change_pass_full_screen.dart';

import 'package:tbs_logistics_phieunghi/app/auth/moduels/change_password_screen.dart';

// ignore: must_be_immutable
class ChangePasswordPage extends GetView<ChangePaswordController> {
  ChangePasswordPage({super.key});

  final String routes = "/CHANGE_PASSWORD_PAGE";
  @override
  var controller = Get.put(ChangePaswordController());
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    if (Get.arguments != null) {
      var username = Get.arguments[0];
      var passwordOld = Get.arguments[1];
      return ChangePasswordScreen(
        oldPass: passwordOld,
        username: username,
      );
    }
    return ChangePasswordFullScreen();
  }
}
