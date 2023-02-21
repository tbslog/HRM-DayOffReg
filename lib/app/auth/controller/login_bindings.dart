import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/auth/controller/login_controller.dart';

class LoginBindins extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut<LoginController>(() => LoginController());
  }
}
