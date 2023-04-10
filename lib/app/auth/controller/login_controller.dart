import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart' hide Response;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:tbs_logistics_phieunghi/app/auth/model/login_model.dart';
import 'package:tbs_logistics_phieunghi/app/auth/model/login_user_model.dart';
import 'package:tbs_logistics_phieunghi/config/core/constants.dart';
import 'package:tbs_logistics_phieunghi/config/routes/pages.dart';

class LoginController extends GetxController {
  late Response response;

  var dio = Dio();

  TextEditingController accountController = TextEditingController(text: "");
  TextEditingController passwordController = TextEditingController(text: "");
  RxBool obcureText = true.obs;

  final formKeyLogin = GlobalKey<FormState>();

  @override
  void onInit() {
    formKeyLogin;
    super.onInit();
  }

  void updateObcureText() {
    obcureText.value = !obcureText.value;
    update();
  }

  void getLogin({
    required String username,
    required String password,
  }) async {
    var user = LoginModel(
      username: username,
      password: password,
      autogen: 0,
    );
    var jsonData = user.toJson();
    String url = "${AppConstants.urlBase}/Login";
    try {
      response = await dio.post(
        url,
        data: jsonData,
        options: Options(
          validateStatus: (_) => true,
        ),
      );

      if (response.statusCode == AppConstants.RESPONSE_CODE_SUCCESS) {
        var jsonRespone = response.data;
        // ignore: unused_local_variable
        var tokens = LoginUserModel.fromJson(jsonRespone);

        if (response.data["rCode"] == 1) {
          Get.defaultDialog(
            barrierDismissible: false,
            title: "Thông báo",
            middleText: "Chưa có tài khoản ! Bạn có muốn tạo tài khoản ?",
            confirmTextColor: Colors.orangeAccent,
            backgroundColor: Colors.white,
            buttonColor: Colors.white,
            cancel: Container(
              height: 35,
              width: 100,
              decoration: BoxDecoration(
                border: Border.all(
                  width: 1,
                  color: Colors.orangeAccent,
                ),
                borderRadius: BorderRadius.circular(15),
              ),
              child: TextButton(
                child: const Text(
                  "Không",
                  style: TextStyle(color: Colors.orangeAccent),
                ),
                onPressed: () {
                  Get.back();
                },
              ),
            ),
            confirm: Container(
              height: 35,
              width: 100,
              decoration: BoxDecoration(
                border: Border.all(
                  width: 1,
                  color: Colors.orangeAccent,
                ),
                borderRadius: BorderRadius.circular(15),
                color: Colors.orangeAccent,
              ),
              child: TextButton(
                child: const Text(
                  "Có",
                  style: TextStyle(color: Colors.white),
                ),
                onPressed: () {
                  createAccount(
                    username: username,
                  );
                  Get.back();
                },
              ),
            ),
          );
        } else if (response.data["rCode"] == 2) {
          passwordController.text = response.data["rData"]["password"];
        } else if (response.data["rCode"] == 0) {
          Get.defaultDialog(
            barrierDismissible: false,
            title: "Thông báo",
            middleText: "Tài khoản hoặc mật khẩu không đúng !",
            confirmTextColor: Colors.orangeAccent,
            backgroundColor: Colors.white,
            onConfirm: () {
              Get.back();
            },
          );
        } else if (response.data["rCode"] == 3) {
          SharedPreferences prefs = await SharedPreferences.getInstance();
          // ignore: unused_local_variable
          var accessToken = await prefs.setString(AppConstants.KEY_ACCESS_TOKEN,
              "${response.data["rData"]["token"]}");
          Get.toNamed(Routes.MANAGER_LEAVE_FORM_SCREEN);
        }
      }
    } catch (e) {
      if (kDebugMode) {
        print(e);
      }
    }
  }

  void createAccount({
    required String username,
  }) async {
    var users = LoginModel(
      username: username,
      password: "",
      autogen: 1,
    );
    var jsonData = users.toJson();
    String url = "${AppConstants.urlBase}/Login";
    try {
      response = await dio.post(url,
          data: jsonData, options: Options(validateStatus: (_) => true));
      if (response.statusCode == 200) {
        // ignore: unused_local_variable
        var jsonRespone = response.data;

        SharedPreferences prefs = await SharedPreferences.getInstance();
        // ignore: unused_local_variable
        var accessToken = await prefs.setString(AppConstants.KEY_ACCESS_TOKEN,
            "${response.data["rData"]["token"]}");
        Get.defaultDialog(
          barrierDismissible: false,
          title: "Thông báo",
          middleText: "",
          content: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text("Tạo thành công :"),
              const SizedBox(
                height: 5,
              ),
              Text(
                "Mật khẩu : ${response.data["rData"]["password"]}",
                style: const TextStyle(color: Colors.red),
              ),
              const SizedBox(
                height: 5,
              ),
              Text("${response.data["rMsg"]}"),
            ],
          ),
          confirmTextColor: Colors.orangeAccent,
          backgroundColor: Colors.white,
          confirm: Container(
            height: 35,
            width: 100,
            decoration: BoxDecoration(
              border: Border.all(
                width: 1,
                color: Colors.orangeAccent,
              ),
              borderRadius: BorderRadius.circular(15),
              color: Colors.orangeAccent,
            ),
            child: TextButton(
              onPressed: () {
                Get.defaultDialog(
                  barrierDismissible: false,
                  title: "Thông báo",
                  middleText: "Bạn có muốn đổi mật khẩu !",
                  confirmTextColor: Colors.orangeAccent,
                  backgroundColor: Colors.white,
                  cancel: Container(
                    height: 35,
                    width: 100,
                    decoration: BoxDecoration(
                      border: Border.all(
                        width: 1,
                        color: Colors.orangeAccent,
                      ),
                      borderRadius: BorderRadius.circular(15),
                      color: Colors.white,
                    ),
                    child: TextButton(
                      onPressed: () {
                        print(response.data["rData"]["token"]);
                        Get.toNamed(Routes.MANAGER_LEAVE_FORM_SCREEN);
                      },
                      child: const Text(
                        "Không",
                        style: TextStyle(color: Colors.orangeAccent),
                      ),
                    ),
                  ),
                  confirm: Container(
                    height: 35,
                    width: 100,
                    decoration: BoxDecoration(
                      border: Border.all(
                        width: 1,
                        color: Colors.orangeAccent,
                      ),
                      borderRadius: BorderRadius.circular(15),
                      color: Colors.orangeAccent,
                    ),
                    child: TextButton(
                      onPressed: () {
                        Get.toNamed(
                          Routes.CHANGE_PASSWORD_SCREEN,
                          arguments: [
                            username,
                            response.data["rData"]["password"]
                          ],
                        );
                      },
                      child: const Text(
                        "Đồng ý",
                        style: TextStyle(
                          color: Colors.white,
                        ),
                      ),
                    ),
                  ),
                );
              },
              child: const Text(
                "Oke",
                style: TextStyle(
                  color: Colors.white,
                ),
              ),
            ),
          ),
          onConfirm: () {
            // Get.back();
          },
        );
      }
    } catch (e) {
      rethrow;
    }
  }

  void getDialog() {
    Get.defaultDialog(
      title: "Loading",
      confirm: CircularProgressIndicator(
        color: Colors.orangeAccent.withOpacity(0.7),
      ),
      middleText: "",
      textConfirm: null,
      confirmTextColor: Colors.white,
      backgroundColor: Colors.white,
      onConfirm: () {
        Get.back();
      },
      buttonColor: Colors.orangeAccent.withOpacity(0.4),
    );
  }

  @override
  void onClose() {
    Get.deleteAll();
    super.onClose();
  }
}
