import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart' hide Response;
import 'package:multi_select_flutter/dialog/mult_select_dialog.dart';
import 'package:multi_select_flutter/util/multi_select_item.dart';
import 'package:multi_select_flutter/util/multi_select_list_type.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/day_of_letter_single_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/departments_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/post_day_off_letter_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/user_model.dart';
import 'package:tbs_logistics_phieunghi/config/core/constants.dart';
import 'package:tbs_logistics_phieunghi/config/share_prefs.dart';

class SingleViewController extends GetxController {
  List<dynamic> selectedDepartments = [];
  var selectedDepartmentsValue = "".obs;
  var selectedDepartmentsId = "".obs;

  List<DepartmentsModel> departments = [
    DepartmentsModel(id: 0, name: "Đơn mới"),
    DepartmentsModel(id: 1, name: "Chờ duyệt"),
    DepartmentsModel(id: 2, name: "Đã duyệt"),
    DepartmentsModel(id: 3, name: "Từ chối"),
  ];

  Future<UserModel> getInfo() async {
    var tokens = await SharePerApi().getToken();
    var dio = Dio();
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

  void showMultiSelect() async {
    await showDialog(
      context: Get.context!,
      builder: (ctx) {
        return MultiSelectDialog(
          height: 250,
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
                    // ignore: prefer_interpolation_to_compose_strings
                    selectedDepartmentsValue.value + element.name + ",";
                selectedDepartmentsId.value =
                    selectedDepartmentsId.value + element.id.toString() + ",";
              },
            );
          },
        );
      },
    );
  }

  Future<List<DayOffLettersSingleModel>> getDayOffLetterSingler(
      {required int needAppr, required String astatus}) async {
    var dio = Dio();
    // var tokens = AppConstants.tokens;
    var tokens = await SharePerApi().getToken();
    Response response;
    Map<String, dynamic> headers = {
      HttpHeaders.authorizationHeader: "Bearer $tokens",
    };
    // ignore: non_constant_identifier_names
    var post_letter =
        PostDayOffLettersModel(needAppr: needAppr, astatus: astatus);
    var jsonData = post_letter.toJson();
    var url = "${AppConstants.urlBase}/day-off-letters?astatus=$astatus";

    try {
      response = await dio.get(
        url,
        options: Options(headers: headers),
      );
      if (response.statusCode == 200) {
        List<dynamic> data = response.data["rData"];

        return data.map((e) => DayOffLettersSingleModel.fromJson(e)).toList();
      }
      return [];
    } catch (e) {
      rethrow;
    }
  }
}
