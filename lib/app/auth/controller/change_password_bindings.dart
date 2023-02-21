import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/auth/controller/change_password_controller.dart';

class ChangePaswordBindings extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut<ChangePaswordController>(() => ChangePaswordController());
  }
}
