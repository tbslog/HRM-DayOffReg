import 'package:get/get.dart';

import 'package:tbs_logistics_phieunghi/config/routes/pages.dart';
import 'package:tbs_logistics_phieunghi/config/share_prefs.dart';

class SplashController extends GetxController {
  @override
  void onInit() {
    Future.delayed(
      const Duration(seconds: 2),
      () => checkUserStatus(),
    );
    super.onInit();
  }

  checkUserStatus() async {
    var tokens = await SharePerApi().getToken();
    if (tokens != null) {
      // Get.toNamed(Routes.LOGIN_PAGE);
      Get.toNamed(Routes.MANAGER_LEAVE_FORM_SCREEN);
    } else {
      Get.toNamed(Routes.LOGIN_PAGE);
    }
  }
}
