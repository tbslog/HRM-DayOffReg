import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/view/access_leave/controller/detail_access_single_controller.dart';

class DetailAccessSingleBindings extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut<DetailAccessSingleController>(
        () => DetailAccessSingleController());
  }
}
