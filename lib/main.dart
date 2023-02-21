import 'dart:io';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';
import 'package:tbs_logistics_phieunghi/app/splash/controller/splash_bindings.dart';
import 'package:tbs_logistics_phieunghi/app/splash/splash_page.dart';
import 'package:tbs_logistics_phieunghi/config/core/constants.dart';
import 'package:tbs_logistics_phieunghi/config/core/language/locale.dart';
import 'package:tbs_logistics_phieunghi/config/core/theme/theme_provider.dart';
import 'package:tbs_logistics_phieunghi/config/routes/pages.dart';

void main() async {
  await GetStorage.init('MyStorage');
  final box = GetStorage('MyStorage');
  String? mode = box.read(AppConstants.THEME_KEY);
  bool isLightMode = (mode != null && mode == "light");
  var locale = const Locale('vi', 'VN');
  Get.updateLocale(locale);
  runApp(
    GetMaterialApp(
      debugShowCheckedModeBanner: false,
      translations: Messages(),
      locale: locale,
      themeMode: isLightMode ? ThemeMode.light : ThemeMode.dark,
      theme: MyThemes.lightTheme,
      darkTheme: MyThemes.lightTheme,
      defaultTransition: Transition.fade,
      initialBinding: SplashBindings(),
      initialRoute: Routes.SPLASH,
      getPages: AppPages.pages,
      home: const SplashScreen(),
    ),
  );
}

class MyHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)
      ..badCertificateCallback =
          (X509Certificate cert, String host, int port) => true;
  }
}
