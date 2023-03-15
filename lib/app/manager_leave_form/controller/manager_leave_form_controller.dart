// ignore_for_file: prefer_interpolation_to_compose_strings

import 'dart:io';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart' hide Response;
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/user_model.dart';
import 'package:tbs_logistics_phieunghi/config/core/constants.dart';
import 'package:tbs_logistics_phieunghi/config/share_prefs.dart';

class ManagerLeaveFormController extends GetxController
    with GetSingleTickerProviderStateMixin {
  var dio = Dio();

  RxBool isChangePage = false.obs;
  RxBool isUserInfo = true.obs;

  final userName = UserModel().obs;

  final List<Tab> myTabs = <Tab>[
    const Tab(text: 'Đơn của tôi'),
    const Tab(text: 'Đơn cần duyệt'),
  ];

  late TabController controller;

  @override
  void onInit() {
    super.onInit();

    getInfo();

    controller = TabController(vsync: this, length: myTabs.length);
  }

  void getInfo() async {
    var tokens = await SharePerApi().getToken();
    Response response;
    Map<String, dynamic> headers = {
      HttpHeaders.authorizationHeader: "Bearer $tokens",
    };
    const url = "${AppConstants.urlBase}/getEmpInfo";
    isUserInfo(false);
    try {
      response = await dio.get(
        url,
        options: Options(headers: headers),
      );
      if (response.statusCode == 200) {
        var data = UserModel.fromJson(response.data["rData"]);

        userName.value = data;
        print(userName.value.jPLevelID);
      }
    } catch (e) {
      rethrow;
    } finally {
      isUserInfo(true);
    }
  }
}
