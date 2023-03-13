// ignore_for_file: unused_local_variable

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/controller/access_leave_form_controller.dart';

// ignore: must_be_immutable
class AccessLeaveFormScreen extends GetView<AccessLeaveFormController> {
  AccessLeaveFormScreen({super.key});

  @override
  var controller = Get.put(AccessLeaveFormController());

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: const [
          Text(
            "Không có dữ liệu !",
            style: TextStyle(
              color: Colors.green,
              fontSize: 18,
            ),
          )
        ],
      ),
    );
  }
}
