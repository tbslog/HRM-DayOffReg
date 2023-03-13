import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart' hide Response;
import 'package:tbs_logistics_phieunghi/app/auth/model/form_change_model.dart';
import 'package:tbs_logistics_phieunghi/config/core/constants.dart';

class ChangePaswordController extends GetxController {
  var dio = Dio();
  late Response response;
  TextEditingController username = TextEditingController(text: "");
  TextEditingController passwordNew = TextEditingController(text: "");
  TextEditingController passwordOld = TextEditingController(text: "");
  TextEditingController rePasswordNew = TextEditingController(text: "");

  var userName = Get.arguments[0];
  var passWord = Get.arguments[1];

  Future<void> changePassword({
    required String newPassword,
    required String confirmPassword,
  }) async {
    const url = "${AppConstants.urlBase}/changePass";

    var changePassword = FormChangePasswordModel(
      username: userName,
      currentPassword: passWord,
      newPassword: newPassword,
      confirmPass: confirmPassword,
    );
    var jsonData = changePassword.toJson();
    try {
      response = await dio.post(
        url,
        data: jsonData,
      );

      if (response.statusCode == AppConstants.RESPONSE_CODE_SUCCESS) {
        var data = response.data;

        Get.snackbar(
          "",
          "",
          backgroundColor: Colors.white,
          titleText: const Text(
            "Thông báo !",
            style: TextStyle(
              color: Colors.red,
            ),
          ),
          messageText: Text(
            "${data["rMsg"]}",
            style: const TextStyle(
              color: Colors.green,
            ),
          ),
          snackPosition: SnackPosition.TOP,
        );
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> changeFullPassword({
    required String userName,
    required String oldPassword,
    required String newPassword,
    required String confirmPassword,
  }) async {
    const url = "${AppConstants.urlBase}/changePass";

    var changePassword = FormChangePasswordModel(
      username: userName,
      currentPassword: oldPassword,
      newPassword: newPassword,
      confirmPass: confirmPassword,
    );
    var jsonData = changePassword.toJson();
    try {
      response = await dio.post(
        url,
        data: jsonData,
      );

      if (response.statusCode == AppConstants.RESPONSE_CODE_SUCCESS) {
        var data = response.data;
        passwordOld.text = "";
        passwordNew.text = "";
        rePasswordNew.text = "";
        Get.snackbar(
          "",
          "",
          backgroundColor: Colors.white,
          titleText: const Text(
            "Thông báo !",
            style: TextStyle(
              color: Colors.red,
            ),
          ),
          messageText: Text(
            "${data["rMsg"]}",
            style: const TextStyle(
              color: Colors.green,
            ),
          ),
          snackPosition: SnackPosition.TOP,
        );
      }
    } catch (e) {
      rethrow;
    }
  }
}
