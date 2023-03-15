import 'package:flutter/material.dart';

import 'package:get/get.dart';
import 'package:intl/intl.dart';

import 'package:tbs_logistics_phieunghi/app/manager_leave_form/view/single_view/controller/single_view_controller.dart';
import 'package:tbs_logistics_phieunghi/config/routes/pages.dart';

class SingleViewManagerScreen extends GetView<SingleViewController> {
  const SingleViewManagerScreen({super.key});
  final String routes = "/SINGLE_VIEW_MANAGER_SCREEN";

  @override
  Widget build(BuildContext context) {
    var day = DateFormat("dd/MM/yyyy");
    Size size = MediaQuery.of(context).size;
    return GetBuilder<SingleViewController>(
      init: SingleViewController(),
      builder: (controller) => Container(
        padding: const EdgeInsets.symmetric(horizontal: 10),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Obx(() {
              return controller.isLoadUser.value
                  ? _buildAdd(
                      onPressed: () {
                        Get.toNamed(Routes.CREATE_LEAVE_FORM_PAGE);
                      },
                      idNV: '${controller.userInfo.value.empID}',
                      userName:
                          '${controller.userInfo.value.lastName} ${controller.userInfo.value.firstName}',
                    )
                  : Container(
                      height: 35,
                      padding: const EdgeInsets.only(left: 10, bottom: 5),
                      decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(30)),
                      child: Row(children: [
                        Expanded(
                          flex: 8,
                          child: Container(
                            height: 30,
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(15),
                            ),
                          ),
                        ),
                        Expanded(
                          flex: 2,
                          child: Container(
                            height: 35,
                            width: 20,
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(100),
                            ),
                          ),
                        ),
                      ]),
                    );
            }),
            const Divider(
              height: 1,
              thickness: 1,
              indent: 5,
              endIndent: 5,
              color: Colors.orangeAccent,
            ),
            Container(
              height: 35,
              padding: const EdgeInsets.only(left: 5),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Obx(
                    () {
                      // var listType = controller.selectedDepartmentsValue.value;

                      return Text(
                        controller.selectedDepartmentsValue.value == ""
                            ? "Danh sách đơn"
                            : controller.selectedDepartmentsValue.value,
                        // : controller.selectedDepartmentsId.value,
                        style: const TextStyle(
                          color: Colors.green,
                          fontWeight: FontWeight.bold,
                          fontSize: 14,
                        ),
                      );
                    },
                  ),
                  SizedBox(
                    height: 35,
                    width: 60,
                    child: IconButton(
                      onPressed: () {
                        controller.selectedDepartmentsId.value = "";
                        controller.selectedDepartmentsValue.value = "";
                        controller.showMultiSelect();
                      },
                      icon: const Icon(
                        Icons.menu,
                        size: 30,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            Obx(() {
              var number = controller.selectedDepartmentsId.value;

              return Expanded(
                  child: controller.isLoadDayOff.value
                      ? ListView.builder(
                          itemCount: controller.listDayOff.length,
                          itemBuilder: (context, index) {
                            var item = controller.listDayOff[index];
                            return _buildCustomListtile(
                              stt: "${index + 1}",
                              dayNow: day.format(
                                DateTime.parse(
                                  item.startDate.toString(),
                                ),
                              ),
                              estimatedDate: day.format(
                                DateTime.parse(
                                  item.comeDate.toString(),
                                ),
                              ),
                              type: '${item.reason}',
                              totalDay: '${item.period} Ngày',
                              status: item.aStatus == 0
                                  ? "Đơn mới"
                                  : item.aStatus == 1
                                      ? "Chờ duyệt"
                                      : item.aStatus == 2
                                          ? "Đã duyệt"
                                          : "Từ chối",
                              color: item.aStatus == 0
                                  ? Colors.green
                                  : item.aStatus == 1
                                      ? Colors.orangeAccent
                                      : item.aStatus == 2
                                          ? Colors.greenAccent
                                          : Colors.red,
                              onTap: () {
                                Get.toNamed(
                                  Routes.DETAIL_SINGLE_VIEW,
                                  arguments: item.regID,
                                );
                              },
                            );
                          })
                      : ListView.builder(
                          itemCount: controller.listDayOff.length,
                          itemBuilder: (context, index) {
                            return Card(
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(10),
                                side: BorderSide(
                                  color: Colors.black.withOpacity(0.4),
                                  width: 1,
                                ),
                              ),
                              child: ListTile(
                                leading: Container(
                                  height: 40,
                                  width: 40,
                                  decoration: BoxDecoration(
                                    color: Colors.black.withOpacity(0.4),
                                    borderRadius: BorderRadius.circular(100),
                                  ),
                                ),
                                title: Row(
                                  mainAxisAlignment: MainAxisAlignment.start,
                                  children: [
                                    Container(
                                      height: 15,
                                      width: size.width * 0.2,
                                      decoration: BoxDecoration(
                                        color: Colors.black.withOpacity(0.3),
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                    ),
                                    const SizedBox(width: 15),
                                    Container(
                                      height: 15,
                                      width: size.width * 0.2,
                                      decoration: BoxDecoration(
                                        color: Colors.black.withOpacity(0.3),
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                    ),
                                  ],
                                ),
                                subtitle: Container(
                                  height: 15,
                                  width: size.width * 0.1,
                                  decoration: BoxDecoration(
                                    color: Colors.black.withOpacity(0.3),
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                ),
                                trailing: Column(
                                  mainAxisAlignment:
                                      MainAxisAlignment.spaceEvenly,
                                  children: [
                                    Container(
                                      height: 15,
                                      width: size.width * 0.15,
                                      decoration: BoxDecoration(
                                        color: Colors.black.withOpacity(0.3),
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                    ),
                                    Container(
                                      height: 15,
                                      width: size.width * 0.15,
                                      decoration: BoxDecoration(
                                        color: Colors.black.withOpacity(0.3),
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            );
                          }));
            }),
          ],
        ),
      ),
    );
  }
}

Widget _buildCustomListtile({
  required String stt,
  required String dayNow,
  required String estimatedDate,
  required String totalDay,
  required String type,
  required String status,
  required Color color,
  required VoidCallback onTap,
}) {
  return Card(
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(10),
      side: const BorderSide(
        color: Colors.orangeAccent,
        width: 1,
      ),
    ),
    child: ListTile(
      onTap: onTap,
      leading: Container(
        height: 40,
        width: 40,
        decoration: BoxDecoration(
          border: Border.all(color: Colors.orangeAccent, width: 1),
          borderRadius: BorderRadius.circular(100),
        ),
        child: Center(child: Text(stt)),
      ),
      title: Row(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          Text(
            "$dayNow - $estimatedDate",
            style: const TextStyle(
              fontSize: 14,
            ),
          ),
        ],
      ),
      subtitle: Text(type),
      trailing: Column(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          Text(totalDay),
          Text(
            status,
            style: TextStyle(color: color),
          ),
        ],
      ),
    ),
  );
}

Widget _buildAdd(
    {required VoidCallback onPressed,
    required String idNV,
    required String userName}) {
  return Container(
    height: 35,
    padding: const EdgeInsets.only(left: 10, bottom: 5),
    decoration: BoxDecoration(borderRadius: BorderRadius.circular(30)),
    child: Row(children: [
      Expanded(
        flex: 8,
        child: Text(
          "$idNV  /  $userName",
          style: const TextStyle(
            fontSize: 18,
          ),
        ),
      ),
      Expanded(
        flex: 2,
        child: InkWell(
          onTap: onPressed,
          child: Container(
            height: 35,
            width: 20,
            decoration: BoxDecoration(
              color: Colors.green,
              borderRadius: BorderRadius.circular(100),
              image: const DecorationImage(
                image: AssetImage("assets/images/add.png"),
              ),
            ),
          ),
        ),
      ),
    ]),
  );
}
