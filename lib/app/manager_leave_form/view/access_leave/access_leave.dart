import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'package:tbs_logistics_phieunghi/app/manager_leave_form/controller/manager_leave_form_controller.dart';

class AccessLeaveScreen extends GetView<ManagerLeaveFormController> {
  const AccessLeaveScreen({super.key});
  final String routes = "/ACCESS_LEAVE_SCREEN";

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: const [
        Center(
          child: Text(
            "Không có quyền !",
            style: TextStyle(color: Colors.red, fontSize: 20),
          ),
        ),
      ],
    );
  }
}
