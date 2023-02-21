import 'package:flutter/material.dart';
import 'package:get/get.dart';

class AccessLeaveFormController extends GetxController
    with GetSingleTickerProviderStateMixin {
  late TabController tabController;
  TextEditingController reasonController = TextEditingController();
  RxBool isHide = false.obs;
  @override
  void onInit() {
    // await refreshSearch();
    tabController = TabController(vsync: this, length: tabCreate.length);
    super.onInit();
  }

  @override
  void onClose() {
    tabController.dispose();
    super.onClose();
  }

  final List<Tab> tabCreate = <Tab>[
    const Tab(text: 'Tạo/Xem'),
    const Tab(text: 'Duyệt'),
  ];
}
