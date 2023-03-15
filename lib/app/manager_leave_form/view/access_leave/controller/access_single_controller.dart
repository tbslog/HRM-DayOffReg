import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart' hide Response;
import 'package:multi_select_flutter/multi_select_flutter.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/approve_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/day_off_letter_manager_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/departments_model.dart';
import 'package:tbs_logistics_phieunghi/config/core/constants.dart';
import 'package:tbs_logistics_phieunghi/config/share_prefs.dart';

class AccessSingleController extends GetxController {
  late Response response;
  var dio = Dio();

  List<dynamic> selectedDepartments = [];
  var selectedDepartmentsValue = "".obs;
  var selectedDepartmentsId = "".obs;
  List<DepartmentsModel> departments = [
    DepartmentsModel(id: 1, name: "Chờ duyệt"),
    DepartmentsModel(id: 2, name: "Đã duyệt"),
    DepartmentsModel(id: 3, name: "Từ chối"),
  ];

  RxList<DayOffLettersManagerModel> listDayOffManager =
      <DayOffLettersManagerModel>[].obs;
  RxBool isLoadDayOffManganer = true.obs;

  @override
  void onInit() {
    getDayOffLetterManager(needAppr: 1, astatus: "");

    super.onInit();
  }

  void getDayOffLetterManager(
      {required int needAppr, required String astatus}) async {
    // var tokens = AppConstants.tokens;
    var tokens = await SharePerApi().getToken();

    Map<String, dynamic> headers = {
      HttpHeaders.authorizationHeader: "Bearer $tokens",
    };
    isLoadDayOffManganer(false);
    var url =
        "${AppConstants.urlBase}/day-off-letters?needAppr=$needAppr&astatus=$astatus";

    try {
      response = await dio.get(
        url,
        options: Options(headers: headers),
      );
      if (response.statusCode == 200) {
        List<dynamic> data = response.data["rData"];

        listDayOffManager.value =
            data.map((e) => DayOffLettersManagerModel.fromJson(e)).toList();
      }
    } catch (e) {
      rethrow;
    } finally {
      Future.delayed(Duration(seconds: 1), () {
        isLoadDayOffManganer(true);
      });
    }
  }

  void showMultiSelect() async {
    await showDialog(
      context: Get.context!,
      builder: (ctx) {
        return MultiSelectDialog(
          height: 200,
          listType: MultiSelectListType.LIST,
          initialValue: selectedDepartments,
          items: departments
              .map((player) =>
                  MultiSelectItem<DepartmentsModel>(player, player.name!))
              .toList(),
          title: const Text("Chọn loại đơn"),
          selectedColor: Colors.blue,
          searchable: true,
          onConfirm: (results) {
            selectedDepartments = results;
            selectedDepartmentsValue.value = "";
            // ignore: avoid_function_literals_in_foreach_calls
            selectedDepartments.forEach(
              (element) {
                selectedDepartmentsValue.value =
                    selectedDepartmentsValue.value + element.name + ",";
                selectedDepartmentsId.value =
                    selectedDepartmentsId.value + element.id.toString() + ",";
              },
            );
            getDayOffLetterManager(
                needAppr: 1, astatus: selectedDepartmentsId.value);
          },
        );
      },
    );
  }

  void postApprove({
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
        // Get.to(() => const AccessLeaveScreen());
        getDayOffLetterManager(astatus: "", needAppr: 1);

        Get.snackbar(
          "Thông báo",
          "${data["rMsg"]} !",
          titleText: const Text(
            "Thông báo",
            style: TextStyle(color: Colors.red),
          ),
          messageText: Text(
            "${data["rMsg"]} !",
            style: const TextStyle(color: Colors.green),
          ),
        );
        update();
      }
    } catch (e) {
      rethrow;
    }
  }
}
