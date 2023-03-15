import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/view/access_leave/controller/access_single_controller.dart';
import 'package:tbs_logistics_phieunghi/config/routes/pages.dart';

class AccessSingleScreen extends GetView<AccessSingleController> {
  const AccessSingleScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // ignore: unused_local_variable
    Size size = MediaQuery.of(context).size;
    var day = DateFormat("dd/MM/yyyy");
    return GetBuilder<AccessSingleController>(
      init: AccessSingleController(),
      builder: (controller) => Padding(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 15),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
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
            Obx(() {
              return Expanded(
                child: controller.isLoadDayOffManganer.value
                    ? controller.listDayOffManager.isNotEmpty
                        ? ListView.builder(
                            padding: const EdgeInsets.only(bottom: 50),
                            itemCount: controller.listDayOffManager.length,
                            itemBuilder: (context, index) {
                              var item = controller.listDayOffManager[index];

                              return _buildCustomListtile(
                                onTap: () {
                                  Get.toNamed(
                                    Routes.DETAIL_ACCESS_SINGLE_SCREEN,
                                    arguments: item.regID,
                                  );
                                },
                                stt: "${index + 1}",
                                fromDay: day.format(
                                  DateTime.parse(
                                    item.startDate.toString(),
                                  ),
                                ),
                                endDay: item.comeDate != null
                                    ? day.format(
                                        DateTime.parse(
                                          item.comeDate.toString(),
                                        ),
                                      )
                                    : "",
                                type: '${item.reason}',
                                totalDay: '${item.period} ngày',
                                color: Colors.green,
                                child: item.aStatus != 1
                                    ? Center(
                                        child: Text(
                                          item.aStatus == 2
                                              ? "Đã duyệt"
                                              : "Từ chối",
                                          style: TextStyle(
                                            color: item.aStatus == 2
                                                ? Colors.green
                                                : Colors.red,
                                          ),
                                        ),
                                      )
                                    : InkWell(
                                        onTap: () {
                                          controller.postApprove(
                                            regID: item.regID!,
                                            comment: "",
                                            state: 1,
                                          );
                                        },
                                        child: Container(
                                          height: 60,
                                          width: 60,
                                          // color: Colors.green,
                                          decoration: BoxDecoration(
                                            // color: Colors.green,
                                            borderRadius:
                                                BorderRadius.circular(10),
                                            image: const DecorationImage(
                                              image: AssetImage(
                                                  "assets/images/check.png"),
                                              fit: BoxFit.fill,
                                            ),
                                          ),
                                        ),
                                      ),
                                msnv: item.empID.toString(),
                                name: "${item.lastName} ${item.firstName}",
                              );
                            })
                        : const Center(
                            child: Text(
                              "Không có đơn !",
                              style: TextStyle(
                                color: Colors.red,
                                fontSize: 20,
                              ),
                            ),
                          )
                    : ListView.builder(
                        itemCount: 6,
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
                        },
                      ),
              );
            }),
            // Obx(() {
            //   var number = controller.selectedDepartmentsId.value;

            //   return Expanded(
            //     child: FutureBuilder(
            //         future: controller.getDayOffLetterSingler(
            //             needAppr: 1, astatus: number),
            //         builder: (context, snapshot) {
            //           if (snapshot.hasData) {
            //             var dayoffletters =
            //                 snapshot.data as List<DayOffLettersSingleModel>;
            //             return dayoffletters.isNotEmpty
            //                 ? ListView.builder(
            //                     padding: const EdgeInsets.only(bottom: 50),
            //                     itemCount: dayoffletters.length,
            //                     itemBuilder: (context, index) {
            //                       var item = dayoffletters[index];

            //                       return _buildCustomListtile(
            //                         onTap: () {
            //                           Get.toNamed(
            //                             Routes.DETAIL_ACCESS_SINGLE_SCREEN,
            //                             arguments: item.regID,
            //                           );
            //                         },
            //                         stt: "${index + 1}",
            //                         fromDay: day.format(
            //                           DateTime.parse(
            //                             item.startDate.toString(),
            //                           ),
            //                         ),
            //                         endDay: item.comeDate != null
            //                             ? day.format(
            //                                 DateTime.parse(
            //                                   item.comeDate.toString(),
            //                                 ),
            //                               )
            //                             : "",
            //                         type: '${item.reason}',
            //                         totalDay: '${item.period} ngày',
            //                         color: Colors.green,
            //                         child: item.aStatus != 1
            //                             ? Center(
            //                                 child: Text(
            //                                   item.aStatus == 2
            //                                       ? "Đã duyệt"
            //                                       : "Từ chối",
            //                                   style: TextStyle(
            //                                     color: item.aStatus == 2
            //                                         ? Colors.green
            //                                         : Colors.red,
            //                                   ),
            //                                 ),
            //                               )
            //                             : InkWell(
            //                                 onTap: () {
            //                                   controller.postApprove(
            //                                     regID: item.regID!,
            //                                     comment: "",
            //                                     state: 1,
            //                                   );
            //                                 },
            //                                 child: Container(
            //                                   height: 60,
            //                                   width: 60,
            //                                   // color: Colors.green,
            //                                   decoration: BoxDecoration(
            //                                     // color: Colors.green,
            //                                     borderRadius:
            //                                         BorderRadius.circular(10),
            //                                     image: const DecorationImage(
            //                                       image: AssetImage(
            //                                           "assets/images/check.png"),
            //                                       fit: BoxFit.fill,
            //                                     ),
            //                                   ),
            //                                 ),
            //                               ),
            //                         msnv: item.empID.toString(),
            //                         name: "${item.lastName} ${item.firstName}",
            //                       );
            //                     })
            //                 : const Center(
            //                     child: Text(
            //                       "Không có đơn !",
            //                       style: TextStyle(
            //                         color: Colors.red,
            //                         fontSize: 20,
            //                       ),
            //                     ),
            //                   );
            //           }
            //           return
            //         }),
            //   );
            // }),
          ],
        ),
      ),
    );
  }

  Widget _buildCustomListtile({
    required String stt,
    required String fromDay,
    required String endDay,
    required String totalDay,
    required String type,
    required Color color,
    required VoidCallback onTap,
    required Widget child,
    required String msnv,
    required String name,
  }) {
    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
        side: const BorderSide(
          color: Colors.orangeAccent,
          width: 1,
        ),
      ),
      child: InkWell(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(
            horizontal: 15,
          ),
          height: 80,
          child: Column(
            children: [
              Expanded(
                flex: 1,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Expanded(
                      flex: 3,
                      child: Text(
                        msnv,
                        textAlign: TextAlign.left,
                      ),
                    ),
                    Expanded(
                      flex: 7,
                      child: Text(
                        name,
                        textAlign: TextAlign.left,
                      ),
                    ),
                  ],
                ),
              ),
              Expanded(
                flex: 2,
                child: Row(
                  children: [
                    Expanded(
                      flex: 8,
                      child: Column(
                        children: [
                          const Divider(
                            height: 1,
                            indent: 0,
                            endIndent: 10,
                            thickness: 1,
                            color: Colors.orangeAccent,
                          ),
                          Expanded(
                            child: Row(
                              children: [
                                Expanded(
                                  flex: 3,
                                  child: Text(
                                    fromDay,
                                    textAlign: TextAlign.left,
                                  ),
                                ),
                                const Expanded(child: Text("-")),
                                Expanded(
                                  flex: 5,
                                  child: Text(
                                    endDay,
                                    textAlign: TextAlign.left,
                                  ),
                                )
                              ],
                            ),
                          ),
                          const Divider(
                            height: 1,
                            indent: 0,
                            endIndent: 10,
                            thickness: 1,
                            color: Colors.orangeAccent,
                          ),
                          Expanded(
                            child: Row(
                              children: [
                                Expanded(
                                  flex: 6,
                                  child: Text(
                                    type,
                                    textAlign: TextAlign.left,
                                  ),
                                ),
                                Expanded(
                                  flex: 4,
                                  child: Text(
                                    totalDay,
                                    textAlign: TextAlign.left,
                                  ),
                                )
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    Expanded(flex: 2, child: child),
                  ],
                ),
              )
            ],
          ),
        ),
      ),
      // child: ListTile(
      //   onTap: onTap,
      //   leading: Container(
      //     height: 40,
      //     width: 40,
      //     decoration: BoxDecoration(
      //       border: Border.all(color: Colors.orangeAccent, width: 1),
      //       borderRadius: BorderRadius.circular(100),
      //     ),
      //     child: Center(child: Text(stt)),
      //   ),
      //   title: Row(
      //     mainAxisAlignment: MainAxisAlignment.start,
      //     children: [
      //       Text(
      //         "$dayNow - $estimatedDate",
      //         style: const TextStyle(
      //           fontSize: 14,
      //         ),
      //       ),
      //     ],
      //   ),
      //   subtitle: Text("$type - $totalDay"),
      //   trailing: Column(
      //     mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      //     children: [
      //       child,
      //     ],
      //   ),
      // ),
    );
  }
}
