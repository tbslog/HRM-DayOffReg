import 'package:flutter/material.dart';

import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/auth/controller/login_controller.dart';
import 'package:tbs_logistics_phieunghi/config/core/data/color.dart';
import 'package:tbs_logistics_phieunghi/config/core/data/validate.dart';

class LoginPage extends GetView<LoginController> {
  const LoginPage({super.key});
  final String routes = "/LOGIN_PAGE";

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    return GetBuilder<LoginController>(
      init: LoginController(),
      builder: (controller) => Scaffold(
        body: SingleChildScrollView(
          child: Container(
            height: size.height,
            decoration: const BoxDecoration(
              gradient: CustomColor.gradient,
            ),
            child: Form(
              key: controller.formKeyLogin,
              autovalidateMode: AutovalidateMode.always,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Container(
                    height: size.height * 0.3,
                    width: size.width,
                    decoration: const BoxDecoration(
                      borderRadius: BorderRadius.only(
                        bottomLeft: Radius.circular(30),
                        bottomRight: Radius.circular(30),
                      ),
                      image: DecorationImage(
                        alignment: Alignment.center,
                        image: AssetImage(
                          "assets/images/background.png",
                        ),
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                  SizedBox(
                    height: size.width * 0.05,
                  ),
                  Container(
                    height: size.height * 0.1,
                    width: size.width,
                    decoration: const BoxDecoration(
                      image: DecorationImage(
                        image: AssetImage("assets/images/logo@2x.png"),
                        fit: BoxFit.contain,
                      ),
                    ),
                  ),
                  SizedBox(
                    height: size.width * 0.05,
                  ),
                  Padding(
                    padding: EdgeInsets.symmetric(
                        horizontal: size.width * 0.1, vertical: 10),
                    child: TextFormField(
                      controller: controller.accountController,
                      validator: (value) => Validate().username(value),
                      decoration: const InputDecoration(
                        icon: Icon(Icons.person),
                        hintText: "Tài khoản",
                        alignLabelWithHint: true,
                        contentPadding: EdgeInsets.symmetric(vertical: 10),
                        labelStyle: TextStyle(color: Colors.black),
                        floatingLabelStyle:
                            TextStyle(color: Colors.black, fontSize: 20),
                        enabledBorder: UnderlineInputBorder(
                          borderSide: BorderSide(
                            color: Colors.greenAccent,
                          ),
                        ),
                        focusedBorder: UnderlineInputBorder(
                          borderSide:
                              BorderSide(color: Colors.orangeAccent, width: 2),
                        ),
                      ),
                    ),
                  ),
                  SizedBox(height: size.width * 0.025),
                  Padding(
                    padding: EdgeInsets.symmetric(
                        horizontal: size.width * 0.1, vertical: 10),
                    child: TextFormField(
                      obscureText: controller.obcureText.value,
                      controller: controller.passwordController,
                      // validator: (value) => Validate().password(value),
                      decoration: InputDecoration(
                        icon: Icon(
                          Icons.lock,
                          color: Colors.black.withOpacity(0.4),
                        ),
                        hintText: "Mật khẩu",
                        suffixIcon: IconButton(
                          onPressed: () {
                            controller.updateObcureText();
                          },
                          icon: controller.obcureText.value == true
                              ? Icon(
                                  Icons.visibility,
                                  color: Colors.black.withOpacity(0.4),
                                )
                              : Icon(
                                  Icons.visibility_off,
                                  color: Colors.black.withOpacity(0.4),
                                ),
                        ),
                        alignLabelWithHint: true,
                        contentPadding:
                            const EdgeInsets.symmetric(vertical: 10),
                        labelStyle: const TextStyle(color: Colors.black),
                        floatingLabelStyle:
                            const TextStyle(color: Colors.black, fontSize: 20),
                        enabledBorder: const UnderlineInputBorder(
                          borderSide: BorderSide(
                            color: Colors.greenAccent,
                          ),
                        ),
                        errorBorder: const UnderlineInputBorder(
                          borderSide: BorderSide(
                            color: Colors.redAccent,
                          ),
                        ),
                        focusedBorder: const UnderlineInputBorder(
                          borderSide:
                              BorderSide(color: Colors.orangeAccent, width: 2),
                        ),
                      ),
                    ),
                  ),
                  SizedBox(height: size.width * 0.05),
                  Container(
                    margin: EdgeInsets.symmetric(
                        horizontal: size.width * 0.05,
                        vertical: size.width * 0.025),
                    decoration: BoxDecoration(
                      color: Colors.orangeAccent.withOpacity(0.8),
                      border: Border.all(
                        width: 1,
                        color: Colors.orangeAccent.withOpacity(0.4),
                      ),
                      borderRadius: const BorderRadius.all(
                        Radius.circular(20.0),
                      ),
                    ),
                    width: size.width * 0.8,
                    height: 60,
                    child: TextButton(
                      onPressed: () {
                        _signUpProcess(
                          context,
                        );
                      },
                      child: const Text(
                        "Đăng nhập",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                  Expanded(child: Container()),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  void _signUpProcess(
    BuildContext context,
    // LoginController controller,
  ) {
    var validate = controller.formKeyLogin.currentState!.validate();

    if (!validate) {
      controller.getLogin(
        username: controller.accountController.text,
        password: controller.passwordController.text,
      );
    }
  }
}
