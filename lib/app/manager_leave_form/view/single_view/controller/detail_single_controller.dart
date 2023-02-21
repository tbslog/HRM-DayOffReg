import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart' hide Response;
import 'package:intl/intl.dart';

import 'package:multi_select_flutter/multi_select_flutter.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/model/list_off_type_model.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/model/register_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/day_of_letter_single_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/departments_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/detail_single_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/post_day_off_letter_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/register_detail_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/user_model.dart';
import 'package:tbs_logistics_phieunghi/config/core/constants.dart';
import 'package:tbs_logistics_phieunghi/config/routes/pages.dart';
import 'package:tbs_logistics_phieunghi/config/share_prefs.dart';

class DetailSingleController extends GetxController {
  TextEditingController timeController = TextEditingController(text: "");
  TextEditingController dayController = TextEditingController();
  TextEditingController reasonController = TextEditingController(text: "");
  TextEditingController addressController = TextEditingController(text: "");
  var selectedDate = DateTime.now().obs;
  var selectedTime = TimeOfDay.now().obs;

  var initialValueReson = "".obs;

  RxList listOffType = [].obs;

  var selectedLoaiPhep = "";
  var dio = Dio();

  List<DepartmentsModel> departments = [
    DepartmentsModel(id: 0, name: "Đơn mới"),
    DepartmentsModel(id: 1, name: "Chờ duyệt"),
    DepartmentsModel(id: 2, name: "Đã duyệt"),
    DepartmentsModel(id: 3, name: "Từ chối"),
  ];
  List<dynamic> selectedDepartments = [];
  var selectedDepartmentsValue = "".obs;
  var selectedDepartmentsId = "".obs;

  void showMultiSelect() async {
    await showDialog(
        context: Get.context!,
        builder: (ctx) {
          return MultiSelectDialog(
            listType: MultiSelectListType.LIST,
            initialValue: selectedDepartments,
            items: departments
                .map((player) =>
                    MultiSelectItem<DepartmentsModel>(player, player.name!))
                .toList(),
            title: const Text("Loại đơn"),
            selectedColor: Colors.blue,
            searchable: true,
            onConfirm: (results) {
              selectedDepartments = results;
              selectedDepartmentsValue.value = "";
              // ignore: avoid_function_literals_in_foreach_calls
              selectedDepartments.forEach((element) {
                selectedDepartmentsValue.value =
                    // ignore: prefer_interpolation_to_compose_strings
                    selectedDepartmentsValue.value + element.name + ",";
                selectedDepartmentsId.value =
                    selectedDepartmentsId.value + element.id.toString();
              });
            },
          );
        });
  }

  void selectDate() async {
    final DateTime? pickedDate = await showDatePicker(
      context: Get.context!,
      initialDate: selectedDate.value,
      firstDate: DateTime.now(),
      lastDate: DateTime(2025),
    );
    if (pickedDate != null && pickedDate != selectedDate.value) {
      selectedDate.value = pickedDate;
      timeController.text =
          DateFormat('yyyy-MM-dd').format(selectedDate.value).toString();
      update();
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

  Future<DetailSingleModel> detailSingle({required int regID}) async {
    var tokens = await SharePerApi().getToken();
    Response response;
    // ignore: unused_local_variable
    Map<String, dynamic> headers = {
      HttpHeaders.authorizationHeader: "Bearer $tokens"
    };
    // ignore: unnecessary_brace_in_string_interps
    var url = "${AppConstants.urlBase}/day-off-letter?regid=${regID}";
    try {
      response = await dio.get(
        url,
        // options: Options(headers: headers),
      );
      if (response.statusCode == AppConstants.RESPONSE_CODE_SUCCESS) {
        var data = DetailSingleModel.fromJson(response.data);
        reasonController.text = data.rData!.reason!;
        addressController.text = data.rData!.address!;
        dayController.text = data.rData!.period!.toString();

        return data;
      }
      return response.data;
    } catch (e) {
      rethrow;
    }
  }

  Future<List<ListOffTypeModel>> getTypeOff(query) async {
    // var tokens = AppConstants.tokens;
    var tokens = await SharePerApi().getToken();
    Response response;
    Map<String, dynamic> headers = {
      HttpHeaders.authorizationHeader: "Bearer $tokens"
    };
    const url = "${AppConstants.urlBase}/${AppConstants.urlListOffType}";
    try {
      response = await dio.get(url,
          options: Options(headers: headers),
          queryParameters: {"query": query});
      if (response.statusCode == 200) {
        List<dynamic> data = response.data["rData"];

        listOffType.value = data;
        update();
        return data.map((e) => ListOffTypeModel.fromJson(e)).toList();
      } else {
        return [];
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<List<DayOffLettersSingleModel>> getDayOffLetterSingler(
      {required int needAppr, required List<String> astatus}) async {
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
    const url = "${AppConstants.urlBase}/day-off-letters";

    try {
      response = await dio.post(
        url,
        options: Options(headers: headers),
        data: jsonData,
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

  Future<void> postRegister({
    required int type,
    required String reason,
    required String startdate,
    required int period,
    required String address,
    required int command,
  }) async {
    // var tokens = AppConstants.tokens;
    var tokens = await SharePerApi().getToken();

    Response response;
    Map<String, dynamic> headers = {
      HttpHeaders.authorizationHeader: "Bearer $tokens"
    };
    var register = RegisterModel(
      type: type,
      reason: reason,
      startdate: startdate,
      period: period,
      address: address,
      command: command,
    );
    var jsonData = register.toJson();
    const url = "${AppConstants.urlBase}/day-off-letter";
    try {
      response = await dio.post(
        url,
        options: Options(headers: headers),
        data: jsonData,
      );

      if (response.statusCode == 200) {
        var data = response.data;
        getDayOffLetterSingler(astatus: [], needAppr: 0);
        if (data["rCode"] == 0) {
          // print("Lỗi");
          Get.snackbar("Thông báo", "${data["rMsg"]} !",
              titleText: const Text(
                "Thông báo",
                style: TextStyle(color: Colors.red),
              ),
              messageText: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: [
                      Text(
                        "${data["rMsg"]} !",
                        style: const TextStyle(color: Colors.green),
                      ),
                    ],
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: [
                      Text(
                        "${data["rError"]} !",
                        style: const TextStyle(color: Colors.green),
                      ),
                    ],
                  ),
                ],
              ));
        } else if (data["rCode"] == 1) {
          Get.snackbar(
            "Thông báo",
            "${data["rMsg"]} !",
            titleText: const Text(
              "Thông báo",
              style: TextStyle(color: Colors.red),
            ),
            messageText: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Text(
                      "${data["rMsg"]}!",
                      textAlign: TextAlign.left,
                      style: const TextStyle(color: Colors.green),
                    )
                  ],
                ),
                const SizedBox(height: 5),
              ],
            ),
            backgroundColor: Colors.white,
          );
          Get.toNamed(Routes.MANAGER_LEAVE_FORM_SCREEN);
        }
        return data;
      }
      update();
    } catch (e) {
      rethrow;
    }
  }

  Future<void> postDetailRegister({
    required int type,
    required int regID,
    required String reason,
    required String startdate,
    required int period,
    required String address,
    required int command,
  }) async {
    // var tokens = AppConstants.tokens;
    var tokens = await SharePerApi().getToken();

    Response response;
    Map<String, dynamic> headers = {
      HttpHeaders.authorizationHeader: "Bearer $tokens"
    };
    var register = RegisterDetailModel(
      regid: regID,
      offtype: type,
      reason: reason,
      startdate: startdate,
      period: period,
      address: address,
      command: command,
    );
    var jsonData = register.toJson();
    const url = "${AppConstants.urlBase}/adjust-day-off";
    try {
      response = await dio.put(
        url,
        options: Options(headers: headers),
        data: jsonData,
      );

      if (response.statusCode == 200) {
        var data = response.data;
        getDayOffLetterSingler(astatus: [], needAppr: 0);
        if (data["rCode"] == 0) {
          // print("Lỗi");
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
        } else if (data["rCode"] == 1) {
          Get.snackbar(
            "Thông báo",
            "${data["rMsg"]} !",
            titleText: const Text(
              "Thông báo",
              style: TextStyle(color: Colors.red),
            ),
            messageText: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Text(
                      "${data["rMsg"]}!",
                      textAlign: TextAlign.left,
                      style: const TextStyle(color: Colors.green),
                    )
                  ],
                ),
                const SizedBox(height: 5),
              ],
            ),
            backgroundColor: Colors.white,
          );
          Get.toNamed(Routes.MANAGER_LEAVE_FORM_SCREEN);
        }
        return data;
      }
      update();
    } catch (e) {
      rethrow;
    }
  }

  // @override
  // void onClose() {
  //   Get.deleteAll();
  //   super.onClose();
  // }
}
