import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart' hide Response;
import 'package:intl/intl.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/model/list_off_type_model.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/model/register_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/user_model.dart';
import 'package:tbs_logistics_phieunghi/config/core/constants.dart';

import 'package:tbs_logistics_phieunghi/config/share_prefs.dart';

class CreateLeaveFormController extends GetxController
    with GetSingleTickerProviderStateMixin {
  TextEditingController timeController = TextEditingController();
  TextEditingController dayController = TextEditingController();
  TextEditingController reasonController = TextEditingController();
  TextEditingController addressController = TextEditingController();
  Rx<UserModel> userName = UserModel().obs;
  late TabController tabController;
  var selectedDate = DateTime.now().obs;
  var selectedTime = TimeOfDay.now().obs;
  var dio = Dio();

  var numberDayFree = "".obs;
  var dayFreeError = RxnString(null);

  var selectedLoaiphep = "";
  var selectedValue = 0.obs;
  var nameType = "".obs;

  RxList listOffType = [].obs;
  GlobalKey<FormState> formKeyCreateLetter = GlobalKey<FormState>();
  var loaiPhep = "";

  RxBool isload = false.obs;
  RxBool isHide = false.obs;
  RxBool isUserInfo = true.obs;

  @override
  void onInit() {
    formKeyCreateLetter;
    getInfo();
    tabController = TabController(vsync: this, length: tabCreate.length);
    super.onInit();
  }

  final List<Tab> tabCreate = <Tab>[
    const Tab(
      text: 'Tạo/Xem',
    ),
    const Tab(
      text: 'Duyệt',
    ),
  ];

  void selectDate() async {
    final DateTime? pickedDate = await showDatePicker(
      context: Get.context!,
      initialDate: selectedDate.value,
      firstDate: DateTime(2023),
      lastDate: DateTime(2025),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            dialogBackgroundColor: Colors.white,
            colorScheme: const ColorScheme.light(
              primary: Colors.orangeAccent,
              onPrimary: Colors.white,
              onSurface: Colors.blueAccent,
            ),
          ),
          child: child!,
        );
      },
    );
    if (pickedDate != null && pickedDate != selectedDate.value) {
      selectedDate.value = pickedDate;
      timeController.text =
          DateFormat('yyyy-MM-dd').format(selectedDate.value).toString();
      update();
    }
  }

  void postRegister({
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
        dayController.text = "";
        reasonController.text = "";
        addressController.text = "";

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
          Get.back();
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
                    ),
                  ],
                ),
                data["rError"] == []
                    ? Row(
                        mainAxisAlignment: MainAxisAlignment.start,
                        children: [
                          Text(
                            "${data["rError"]["startdate"]}!",
                            textAlign: TextAlign.left,
                            style: const TextStyle(color: Colors.green),
                          ),
                        ],
                      )
                    : Container(),
                const SizedBox(height: 5),
              ],
            ),
            backgroundColor: Colors.white,
          );
        }
      }
    } catch (e) {
      rethrow;
    }
  }

  void getInfo() async {
    var dio = Dio();

    isUserInfo(false);

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

        userName.value = data;
      }
    } catch (e) {
      rethrow;
    } finally {
      Future.delayed(const Duration(seconds: 1), () {
        isUserInfo(true);
      });
    }
  }

  Future<List<ListOffTypeModel>> getTypeOff(query) async {
    // var tokens = AppConstants.tokens;
    var tokens = SharePerApi().getToken();
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
        // ignore: unused_local_variable
        var result =
            data.map((e) => ListOffTypeModel.fromJson(e).note).toList();

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
}
