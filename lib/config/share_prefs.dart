import 'package:get/get.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:tbs_logistics_phieunghi/config/core/constants.dart';

class SharePerApi {
  Future<dynamic> getToken() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    var token = prefs.getString(AppConstants.KEY_ACCESS_TOKEN);
    return token;
  }

  Future<void> postLogout() async {
    SharedPreferences pref = await SharedPreferences.getInstance();
    pref.remove(AppConstants.KEY_ACCESS_TOKEN);

    Get.toNamed("/LOGIN_PAGE");
  }
}
