import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/controller/manager_leave_form_controller.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/user_model.dart';

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
                          // mainAxisAlignment: MainAxisAlignment.end,
                          children: [
                            Container(
                              height: size.width * 0.2,
                              width: size.width * 0.2,
                              decoration: BoxDecoration(
                                border:
                                    Border.all(color: Colors.white, width: 1),
                                borderRadius: BorderRadius.circular(100),
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
                              height: size.width * 0.2,
                            ),
                            FutureBuilder(
                                future: controller.getInfo(),
                                builder: (context, snapshot) {
                                  if (snapshot.hasData) {
                                    var items = snapshot.data as UserModel;
                                    return Column(
                                      children: [
                                        Text(
                                          "Họ và tên : ${items.lastName} ${items.firstName}",
                                          style: const TextStyle(
                                              color: Colors.orangeAccent),
                                        ),
                                        const SizedBox(
                                          height: 10,
                                        ),
                                        Text(
                                          "MSNV : ${items.empID}",
                                          style: const TextStyle(
                                              color: Colors.orangeAccent),
                                        ),
                                      ],
                                    );
                                  }
                                  return Column(
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
              ),
            ));
  }
}
