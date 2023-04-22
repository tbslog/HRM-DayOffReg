import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/changes_password/controller/change_password_full_controller.dart';

class ChangePaswordBindingsFull extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut<ChangePasswordFullController>(
        () => ChangePasswordFullController());
  }
}
