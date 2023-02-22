import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'package:tbs_logistics_phieunghi/app/splash/controller/splash_controller.dart';

class SplashScreen extends GetView<SplashController> {
  const SplashScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return GetBuilder<SplashController>(
      init: SplashController(),
      builder: (controller) {
        return Image.asset("assets/images/logo@2x.png");
      },
    );
  }
}
