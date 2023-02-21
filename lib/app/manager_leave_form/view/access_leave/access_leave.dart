import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/controller/manager_leave_form_controller.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/day_off_letter_manager_model.dart';

class AccessLeaveScreen extends GetView<ManagerLeaveFormController> {
  const AccessLeaveScreen({super.key});
  final String routes = "/ACCESS_LEAVE_SCREEN";

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    var day = DateFormat("dd/MM/yyyy");
    return GetBuilder<ManagerLeaveFormController>(
      init: ManagerLeaveFormController(),
      builder: (controller) => SizedBox(
        height: size.height,
        child: Stack(
          children: <Widget>[
            Container(
              padding: const EdgeInsets.only(bottom: 15),
              child: controller.expiringContractStatus.isEmpty
                  ? const CircularProgressIndicator()
                  : Column(
                      mainAxisAlignment: MainAxisAlignment.start,
                      children: [
                        Expanded(
                          child: FutureBuilder(
                              future: controller.getDayOffLetterManager(
                                  needAppr: 1, astatus: []),
                              builder: (context, snapshot) {
                                if (snapshot.hasData) {
                                  var dayoffletters = snapshot.data
                                      as List<DayOffLettersManagerModel>;
                                  return ListView.builder(
                                      scrollDirection: Axis.vertical,
                                      itemCount: dayoffletters.length,
                                      itemBuilder: (context, index) {
                                        var item = dayoffletters[index];
                                        return _buildCustomListtile(
                                          stt: "$index",
                                          dayNow: day.format(
                                            DateTime.parse(
                                              item.startDate.toString(),
                                            ),
                                          ),
                                          estimatedDate: day.format(
                                            DateTime.parse(
                                              item.regDate.toString(),
                                            ),
                                          ),
                                          type: '${item.reason}',
                                          totalDay: '${item.period} Ngày',
                                          status: item.aStatus == 0
                                              ? "Chờ mới"
                                              : item.aStatus == 1
                                                  ? "Chờ duyệt"
                                                  : item.aStatus == 2
                                                      ? "Đã duyệt"
                                                      : "Từ chối",
                                          color: Colors.green,
                                        );
                                      });
                                }
                                return const Center(
                                  child: CircularProgressIndicator(),
                                );
                              }),
                        ),
                        const SizedBox(
                          height: 50,
                        ),
                      ],
                    ),
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
  }) {
    return Card(
      child: ListTile(
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
}
