import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/controller/manager_leave_form_controller.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/view/access_leave/access_single_screen.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/view/single_view/single_view.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/view/widgets/drawer.dart';
import 'package:tbs_logistics_phieunghi/config/core/data/color.dart';
import 'package:tbs_logistics_phieunghi/config/core/data/text_style.dart';

import 'view/access_leave/access_leave.dart';

class ManagerLeaveFormScreen extends GetView<ManagerLeaveFormController> {
  const ManagerLeaveFormScreen({super.key});
  final String routes = "/MANAGER_LEAVE_FORM_SCREEN";

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    return GetBuilder<ManagerLeaveFormController>(
        init: ManagerLeaveFormController(),
        builder: (controller) {
          return DefaultTabController(
            length: 2,
            child: Scaffold(
              appBar: AppBar(
                title: const Text(
                  "Quản lý đơn nghỉ phép",
                  style: CustomTextStyle.tilteAppbar,
                ),
                backgroundColor: CustomColor.backgroundAppbar,
                centerTitle: true,
                // automaticallyImplyLeading: false,
              ),
              drawer: const Drawer(
                child: MenuDrawer(),
              ),
              body: SingleChildScrollView(
                child: Container(
                  height: size.height,
                  width: size.width,
                  padding: const EdgeInsets.symmetric(vertical: 15),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: [
                      Container(
                        height: 50,
                        decoration: BoxDecoration(
                          color: Colors.grey[300],
                          borderRadius: BorderRadius.circular(
                            25.0,
                          ),
                        ),
                        child: TabBar(
                          controller: controller.controller,
                          indicator: BoxDecoration(
                            borderRadius: BorderRadius.circular(
                              25.0,
                            ),
                            color: Colors.orangeAccent.shade200,
                          ),
                          labelColor: Colors.white,
                          unselectedLabelColor: Colors.black,
                          tabs: controller.myTabs,
                        ),
                      ),
                      const SizedBox(height: 10),
                      Obx(() {
                        return Expanded(
                          child: TabBarView(
                            controller: controller.controller,
                            children: [
                              const SingleViewManagerScreen(),
                              controller.userName.value.jPLevelID == 70 ||
                                      controller.userName.value.jPLevelID ==
                                          71 ||
                                      controller.userName.value.jPLevelID ==
                                          72 ||
                                      controller.userName.value.jPLevelID == 73
                                  ? const AccessLeaveScreen()
                                  : const AccessSingleScreen()
                            ],
                          ),
                        );
                      })
                    ],
                  ),
                ),
              ),
            ),
          );
        });
  }
}
