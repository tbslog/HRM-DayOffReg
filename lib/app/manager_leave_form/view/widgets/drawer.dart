import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/controller/manager_leave_form_controller.dart';
import 'package:tbs_logistics_phieunghi/config/routes/pages.dart';

import 'package:tbs_logistics_phieunghi/config/share_prefs.dart';

class MenuDrawer extends StatelessWidget {
  const MenuDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    return GetBuilder<ManagerLeaveFormController>(
        builder: (controller) => Container(
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                    colors: [Colors.black, Colors.white],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                    stops: [1, 0.4]),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Stack(
                    children: [
                      SizedBox(
                        height: size.width * 0.6,
                        width: size.width,
                        child: Image.asset(
                          "assets/images/background_user.png",
                          fit: BoxFit.cover,
                        ),
                      ),
                      Positioned(
                        bottom: 0,
                        right: 0,
                        left: 0,
                        child: Column(
                          children: [
                            Obx(() {
                              return controller.isUserInfo.value
                                  ? Column(
                                      children: [
                                        Container(
                                          height: size.width * 0.2,
                                          width: size.width * 0.2,
                                          decoration: BoxDecoration(
                                            border: Border.all(
                                                color: Colors.white, width: 1),
                                            borderRadius:
                                                BorderRadius.circular(100),
                                            image: const DecorationImage(
                                              image: AssetImage(
                                                "assets/images/person.png",
                                              ),
                                            ),
                                          ),

                                          // child: Image.asset(
                                          //   "assets/images/person.png",
                                          //   fit: BoxFit.cover,
                                          // ),
                                        ),
                                        SizedBox(
                                          height: size.width * 0.1,
                                        ),
                                        Text(
                                          "Họ và tên : ${controller.userName.value.lastName} ${controller.userName.value.firstName}",
                                          style: const TextStyle(
                                              color: Colors.orangeAccent),
                                        ),
                                        const SizedBox(
                                          height: 10,
                                        ),
                                        Text(
                                          "MSNV : ${controller.userName.value.empID}",
                                          style: const TextStyle(
                                              color: Colors.orangeAccent),
                                        ),
                                        const SizedBox(
                                          height: 10,
                                        ),
                                        Text(
                                          "Bộ phận : ${controller.userName.value.jobpositionName}",
                                          style: const TextStyle(
                                              color: Colors.orangeAccent),
                                        ),
                                      ],
                                    )
                                  : Column(
                                      children: [
                                        Container(
                                          height: 15,
                                          width: size.width * 0.3,
                                          decoration: BoxDecoration(
                                              color:
                                                  Colors.white.withOpacity(0.4),
                                              borderRadius:
                                                  BorderRadius.circular(10)),
                                        ),
                                        const SizedBox(
                                          height: 10,
                                        ),
                                        Container(
                                          height: 15,
                                          width: size.width * 0.4,
                                          decoration: BoxDecoration(
                                              color:
                                                  Colors.white.withOpacity(0.4),
                                              borderRadius:
                                                  BorderRadius.circular(10)),
                                        ),
                                      ],
                                    );
                            }),
                          ],
                        ),
                      ),
                    ],
                  ),
                  Column(
                    children: [
                      Card(
                        color: Colors.black,
                        child: ListTile(
                          onTap: () {
                            Get.toNamed(Routes.CHANGE_PASSWORD_PAGE);
                          },
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10),
                            side: const BorderSide(color: Colors.orangeAccent),
                          ),
                          title: const Text(
                            "Đổi Password",
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: Colors.orangeAccent,
                            ),
                          ),
                          trailing: const Icon(
                            Icons.lock,
                            color: Colors.orangeAccent,
                          ),
                        ),
                      ),
                      const SizedBox(height: 10),
                      Card(
                        color: Colors.black,
                        child: ListTile(
                          onTap: () async {
                            await SharePerApi().postLogout();
                          },
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10),
                            side: const BorderSide(color: Colors.orangeAccent),
                          ),
                          title: const Text(
                            "Đăng xuất",
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: Colors.orangeAccent,
                            ),
                          ),
                          trailing: const Icon(
                            Icons.logout_outlined,
                            color: Colors.orangeAccent,
                          ),
                        ),
                      )
                    ],
                  )
                ],
              ),
            ));
  }
}
