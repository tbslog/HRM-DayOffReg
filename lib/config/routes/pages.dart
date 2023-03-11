import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/auth/moduels/change_pass_full_screen.dart';
import 'package:tbs_logistics_phieunghi/app/auth/moduels/change_password_screen.dart';
import 'package:tbs_logistics_phieunghi/app/auth/view/change_passwod_page.dart';

import 'package:tbs_logistics_phieunghi/app/auth/view/login_page.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/view/create_leave_form_page.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/view/create_leave_form/create_leave_form_screen.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/manager_leave_form_page.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/view/access_leave/detail_access_single_screen.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/view/single_view/single_view.dart';
import 'package:tbs_logistics_phieunghi/app/splash/controller/splash_bindings.dart';
import 'package:tbs_logistics_phieunghi/app/splash/splash_page.dart';

import '../../app/manager_leave_form/view/access_leave/access_leave.dart';
import '../../app/manager_leave_form/view/single_view/detail_single_view.dart';

part 'routes.dart';

abstract class AppPages {
  static final pages = [
    //Login
    GetPage(
      name: Routes.LOGIN_PAGE,
      page: () => LoginPage(),
    ),
    GetPage(
      name: Routes.SPLASH,
      page: () => const SplashScreen(),
      binding: SplashBindings(),
    ),
    GetPage(
      name: Routes.CHANGE_PASSWORD_PAGE,
      page: () => ChangePasswordPage(),
    ),
    GetPage(
      name: Routes.CHANGE_PASSWORD_SCREEN,
      page: () => ChangePasswordScreen(
        oldPass: '',
        username: '',
      ),
    ),
    GetPage(
      name: Routes.CHANGE_PASSWORD__FULL_SCREEN,
      page: () => ChangePasswordFullScreen(),
    ),
    //MANAGER_LEAVE
    GetPage(
      name: Routes.MANAGER_LEAVE_FORM_SCREEN,
      page: () => const ManagerLeaveFormScreen(),
    ),
    GetPage(
      name: Routes.ACCESS_LEAVE_SCREEN,
      page: () => const AccessLeaveScreen(),
    ),
    GetPage(
      name: Routes.SINGLE_VIEW_MANAGER_SCREEN,
      page: () => const SingleViewManagerScreen(),
    ),
    GetPage(
      name: Routes.DETAIL_SINGLE_VIEW,
      page: () => DetailSingleView(),
    ),
    GetPage(
        name: Routes.DETAIL_ACCESS_SINGLE_SCREEN,
        page: () => const DetailAccessSingleScreen()),
    //CREATE_LEAVE
    GetPage(
      name: Routes.CREATE_LEAVE_FORM_SCREEN,
      page: () => const CreateLeaveFormScreen(),
    ),
    GetPage(
      name: Routes.CREATE_LEAVE_FORM_PAGE,
      page: () => const CreateLeaveFormPage(),
    ),
  ];
}
