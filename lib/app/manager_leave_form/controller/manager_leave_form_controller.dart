import 'dart:io';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart' hide Response;
import 'package:multi_select_flutter/dialog/mult_select_dialog.dart';
import 'package:multi_select_flutter/util/multi_select_item.dart';
import 'package:multi_select_flutter/util/multi_select_list_type.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/approve_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/day_of_letter_single_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/day_off_letter_manager_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/departments_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/detail_single_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/post_day_off_letter_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/user_model.dart';
import 'package:tbs_logistics_phieunghi/config/core/constants.dart';
import 'package:tbs_logistics_phieunghi/config/share_prefs.dart';

class ManagerLeaveFormController extends GetxController
    with GetSingleTickerProviderStateMixin {
  var dio = Dio();

  RxBool isChangePage = false.obs;
  // RxList<DayOffLettersModel> dayoffletters = <DayOffLettersModel>[].obs;
  final userName = UserModel().obs;

  final List<Tab> myTabs = <Tab>[
    const Tab(text: 'Đơn của tôi'),
    const Tab(text: 'Đơn cần duyệt'),
  ];

  final expiringContractStatus = <Map>[
    {"title": "aaa", "isCheck": false},
    {"title": "bbb", "isCheck": false},
    {"title": "ccc", "isCheck": false}
  ].obs;

  List<DepartmentsModel> departments = [
    DepartmentsModel(id: 1, name: "Chờ duyệt"),
    DepartmentsModel(id: 2, name: "Đã duyệt"),
    DepartmentsModel(id: 3, name: "Từ chối"),
  ];
  List<dynamic> selectedDepartments = [];
  var selectedDepartmentsValue = "".obs;
  var selectedDepartmentsId = "".obs;

  void itemChange(bool value, int index) {
    expiringContractStatus[index]["isCheck"] = value;
    update();
  }

  late TabController controller;

  @override
  void onInit() {
    super.onInit();
    // getDayOffLetter();
    getInfo();
    update();
    controller = TabController(vsync: this, length: myTabs.length);
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
                    // ignore: prefer_interpolation_to_compose_strings
                    selectedDepartmentsValue.value + element.name + ",";
                selectedDepartmentsId.value =
                    selectedDepartmentsId.value + element.id.toString();
              },
            );
          },
        );
      },
    );
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

        // ignore: unnecessary_cast
        return data as UserModel;
      }
      return response.data;
    } catch (e) {
      rethrow;
    }
  }

  Future<List<DayOffLettersManagerModel>> getDayOffLetterManager(
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

        return data.map((e) => DayOffLettersManagerModel.fromJson(e)).toList();
      }
      return [];
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
        // var detail = data.rData;

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
        // Get.to(() => const AccessLeaveScreen());
        getDayOffLetterSingler(astatus: [], needAppr: 1);

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

  @override
  void onClose() {
    Get.deleteAll();
    // controller.dispose();
    super.onClose();
  }
}
