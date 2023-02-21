import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/controller/create_leave_controller.dart';

class CreateLeaveBindings extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut<CreateLeaveController>(() => CreateLeaveController());
  }
}
