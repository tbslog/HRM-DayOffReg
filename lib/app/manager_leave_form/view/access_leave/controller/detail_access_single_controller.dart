import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart' hide Response;
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/approve_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/detail_single_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/user_model.dart';
import 'package:tbs_logistics_phieunghi/config/core/constants.dart';
import 'package:tbs_logistics_phieunghi/config/routes/pages.dart';
import 'package:tbs_logistics_phieunghi/config/share_prefs.dart';

class DetailAccessSingleController extends GetxController
    with GetSingleTickerProviderStateMixin {
  var dio = Dio();
  late TabController tabController;
  TextEditingController reasonManagerController = TextEditingController();
  @override
  void onInit() {
    // await refreshSearch();
    tabController = TabController(vsync: this, length: tabCreate.length);
    super.onInit();
  }

  final List<Tab> tabCreate = <Tab>[
    const Tab(text: 'Xem'),
    const Tab(text: 'Duyệt'),
  ];

  Future<DetailSingleModel> detailSingle({required int regID}) async {
    var tokens = await SharePerApi().getToken();
    Response response;
    Map<String, dynamic> headers = {
      HttpHeaders.authorizationHeader: "Bearer $tokens"
    };
    // ignore: unnecessary_brace_in_string_interps
    var url = "${AppConstants.urlBase}/day-off-letter?regid=${regID}";

    try {
      response = await dio.get(
        url,
        options: Options(headers: headers),
      );
      if (response.statusCode == AppConstants.RESPONSE_CODE_SUCCESS) {
        var data = DetailSingleModel.fromJson(response.data);
        return data;
      }
      return response.data;
    } catch (e) {
      rethrow;
    }
  }

  Future<UserModel> getInfo() async {
    var tokens = await SharePerApi().getToken();

    Response response;
    Map<String, dynamic> headers = {
      HttpHeaders.authorizationHeader: "Bearer $tokens",
    };
    const url = "${AppConstants.urlBase}/getEmpInfo";
    try {
      response = await dio.get(
        url,
        options: Options(headers: headers),
      );
      if (response.statusCode == 200) {
        var data = UserModel.fromJson(response.data["rData"]);

        return data;
      }
      return response.data;
    } catch (e) {
      rethrow;
    }
  }

  Future<UserModel> getInfoClient({required String empId}) async {
    var tokens = await SharePerApi().getToken();

    Response response;
    Map<String, dynamic> headers = {
      HttpHeaders.authorizationHeader: "Bearer $tokens",
    };
    var url = "${AppConstants.urlBase}/getEmpInfo?empId=$empId";
    try {
      response = await dio.get(
        url,
        options: Options(headers: headers),
      );
      if (response.statusCode == 200) {
        var data = UserModel.fromJson(response.data["rData"]);

        return data;
      }
      return response.data;
    } catch (e) {
      rethrow;
    }
  }

  Future<void> postApprove({
    required int regID,
    required String comment,
    required int state,
  }) async {
    Response response;
    var tokens = await SharePerApi().getToken();
    Map<String, dynamic> headers = {
      HttpHeaders.authorizationHeader: "Bearer $tokens",
    };
    var approve = ApproveModel(
      regid: regID,
      comment: comment,
      state: state,
    );
    var jsonData = approve.toJson();
    const url = "${AppConstants.urlBase}/approve";
    try {
      response = await dio.post(url,
          options: Options(headers: headers), data: jsonData);
      if (response.statusCode == AppConstants.RESPONSE_CODE_SUCCESS) {
        var data = response.data;
        if (data["rCode"] == 0) {
          Get.snackbar(
            "Thông báo",
            "${data["rMsg"][0]} !",
            titleText: const Text(
              "Thông báo",
              style: TextStyle(color: Colors.red),
            ),
            messageText: Text(
              "${data["rMsg"][0]} !",
              style: const TextStyle(color: Colors.green),
            ),
          );
        } else if (data["rCode"] == 1) {
          Get.toNamed(Routes.MANAGER_LEAVE_FORM_SCREEN);
          Get.snackbar(
            "Thông báo",
            "${data["rMsg"][0]} !",
            titleText: const Text(
              "Thông báo",
              style: TextStyle(color: Colors.red),
            ),
            messageText: Text(
              "${data["rMsg"][0]} !",
              style: const TextStyle(color: Colors.green),
            ),
          );
        }
      }
    } catch (e) {
      rethrow;
    }
  }
}
