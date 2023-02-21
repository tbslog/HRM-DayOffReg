// ignore_for_file: non_constant_identifier_names

import 'package:flutter/material.dart';

import 'package:get/get.dart';
import 'package:intl/intl.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/day_of_letter_single_model.dart';

import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/user_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/view/single_view/controller/detail_single_controller.dart';
import 'package:tbs_logistics_phieunghi/config/routes/pages.dart';

class SingleViewManagerScreen extends GetView<DetailSingleController> {
  const SingleViewManagerScreen({super.key});
  final String routes = "/SINGLE_VIEW_MANAGER_SCREEN";

  @override
  Widget build(BuildContext context) {
    var day = DateFormat("dd/MM/yyyy");
    return GetBuilder<DetailSingleController>(
      init: DetailSingleController(),
      builder: (controller) => Container(
        padding: const EdgeInsets.symmetric(horizontal: 10),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            FutureBuilder(
                future: controller.getInfo(),
                builder: (context, snapshot) {
                  if (snapshot.hasData) {
                    var items = snapshot.data as UserModel;
                    return _buildAdd(
                      onPressed: () {
                        Get.toNamed(Routes.CREATE_LEAVE_FORM_PAGE);
                      },
                      MSNV: '${items.empID}',
                      UserName: '${items.lastName} ${items.firstName}',
                    );
                  }
                  return const Center(
                    child: CircularProgressIndicator(),
                  );
                }),
            const SizedBox(height: 15),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Obx(
                  () {
                    // ignore: unused_local_variable
                    var listType = controller.selectedDepartmentsValue.value;

                    return Text(
                      controller.selectedDepartmentsValue.value,
                      style: const TextStyle(
                        color: Colors.green,
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                      ),
                    );
                  },
                ),
                ElevatedButton(
                  style: ButtonStyle(
                    backgroundColor:
                        MaterialStateProperty.all<Color>(Colors.orangeAccent),
                  ),
                  onPressed: () {
                    controller.selectedDepartmentsId.value = "";
                    controller.selectedDepartmentsValue.value = "";
                    controller.showMultiSelect();
                  },
                  child: const Text('Chọn loại phép'),
                ),
              ],
            ),
            const SizedBox(height: 15),
            Obx(
              () {
                var number = controller.selectedDepartmentsId.value;
                var listNumber = number.split("");
                return Expanded(
                  child: FutureBuilder(
                      future: controller.getDayOffLetterSingler(
                          needAppr: 0, astatus: listNumber),
                      builder: (context, snapshot) {
                        if (snapshot.hasData) {
                          var dayoffletters =
                              snapshot.data as List<DayOffLettersSingleModel>;

                          return ListView.builder(
                              itemCount: dayoffletters.length,
                              itemBuilder: (context, index) {
                                var item = dayoffletters[index];
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
                              });
                        }
                        return const Center(
                          child: CircularProgressIndicator(),
                        );
                      }),
                );
              },
            ),
          ],
        ),
      ),
    );
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
      required String MSNV,
      required String UserName}) {
    return ListTile(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
        side: const BorderSide(
          color: Colors.orangeAccent,
          width: 1,
        ),
      ),
      title: Text("$MSNV  /  $UserName"),
      trailing: Container(
        decoration: BoxDecoration(
          color: Colors.green,
          borderRadius: BorderRadius.circular(100),
        ),
        child: IconButton(
          onPressed: onPressed,
          icon: const Icon(
            Icons.add_circle_outlined,
            color: Colors.white,
            size: 30,
          ),
        ),
      ),
    );
  }
}
