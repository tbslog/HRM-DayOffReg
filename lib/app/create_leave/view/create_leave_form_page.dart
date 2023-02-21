import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/controller/create_leave_controller.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/view/create_leave_form/access_leave_form_screen.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/view/create_leave_form/create_leave_form_screen.dart';
import 'package:tbs_logistics_phieunghi/config/core/data/color.dart';
import 'package:tbs_logistics_phieunghi/config/core/data/text_style.dart';

class CreateLeaveFormPage extends GetView<CreateLeaveController> {
  const CreateLeaveFormPage({super.key});
  final String routes = "/CREATE_LEAVE_FORM_PAGE";
  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    return GetBuilder<CreateLeaveController>(
        init: CreateLeaveController(),
        builder: (controller) {
          return DefaultTabController(
            length: 2,
            child: Scaffold(
              resizeToAvoidBottomInset: false,
              appBar: AppBar(
                title: const Text(
                  "Quản lý đơn nghỉ phép",
                  style: CustomTextStyle.tilteAppbar,
                ),
                backgroundColor: CustomColor.backgroundAppbar,
                centerTitle: true,
                leading: IconButton(
                  onPressed: () {
                    Get.back();
                  },
                  icon: const Icon(
                    Icons.arrow_back_ios_new_outlined,
                  ),
                ),
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
                          controller: controller.tabController,
                          // give the indicator a decoration (color and border radius)
                          indicator: BoxDecoration(
                            borderRadius: BorderRadius.circular(
                              25.0,
                            ),
                            color: Colors.orangeAccent.shade200,
                          ),
                          labelColor: Colors.white,
                          unselectedLabelColor: Colors.black,
                          tabs: controller.tabCreate,
                        ),
                      ),
                      const SizedBox(height: 10),
                      Expanded(
                        child: TabBarView(
                          controller: controller.tabController,
                          children: [
                            const CreateLeaveFormScreen(),
                            // ignore: unrelated_type_equality_checks
                            controller.isload == false
                                ? AccessLeaveFormScreen()
                                : const CreateLeaveFormScreen(),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          );
        });
  }
}
