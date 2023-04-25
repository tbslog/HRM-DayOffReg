import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart' hide Response;
import 'package:tbs_logistics_phieunghi/app/changes_password/model/form_change_model.dart';
import 'package:tbs_logistics_phieunghi/config/core/constants.dart';

class ChangePasswordFullController extends GetxController {
  var dio = Dio();
  late Response response;

  TextEditingController passwordNew = TextEditingController();
  TextEditingController passwordOld = TextEditingController();
  TextEditingController rePasswordNew = TextEditingController();

  final GlobalKey<FormState> formKeyChangePassFull = GlobalKey<FormState>();

  var empID = 0.obs;

  @override
  void onInit() {
    formKeyChangePassFull;
    var idEmp = Get.arguments;
    empID.value = idEmp;
    super.onInit();
  }

  void changeFullPassword({
    required String oldPassword,
    required String newPassword,
    required String confirmPassword,
  }) async {
    const url = "${AppConstants.urlBase}/changePass";

    var changePassword = FormChangePasswordModel(
      username: "${empID.value}",
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
        if (data["rCode"] == 1) {
          Get.back();
          getSnack(data["rMsg"]);
        }
        {
          getSnack(data["rMsg"]);
        }
      }
    } catch (e) {
      rethrow;
    }
  }

  void getSnack(String messageText) {
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
        messageText,
        style: const TextStyle(
          color: Colors.green,
        ),
      ),
      snackPosition: SnackPosition.TOP,
    );
  }
}
