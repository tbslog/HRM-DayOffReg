import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/splash/controller/splash_controller.dart';

class SplashBindings extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut<SplashController>(() => SplashController());
  }
}
