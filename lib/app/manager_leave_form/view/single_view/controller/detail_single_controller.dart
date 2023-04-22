// ignore_for_file: unnecessary_brace_in_string_interps

import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart' hide Response;
import 'package:intl/intl.dart';
import 'package:tbs_logistics_phieunghi/app/create_leave/model/list_off_type_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/day_of_letter_single_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/detail_single_model.dart';
import 'package:tbs_logistics_phieunghi/app/manager_leave_form/model/register_detail_model.dart';
import 'package:tbs_logistics_phieunghi/config/core/constants.dart';

import 'package:tbs_logistics_phieunghi/config/share_prefs.dart';

class DetailSingleController extends GetxController {
  var selectedDate = DateTime.now().obs;
  var selectedTime = TimeOfDay.now().obs;

  var initialValueReson = "".obs;

  RxList listOffType = [].obs;
  RxList typeOff = [].obs;

  var selectedLoaiPhep = "";
  var dio = Dio();

  var selectedValue = 0.obs;
  var nameType = "".obs;

  GlobalKey<FormState> formDetail = GlobalKey<FormState>();

  TextEditingController timeController = TextEditingController();

  TextEditingController dayController = TextEditingController();
  TextEditingController reasonController = TextEditingController();
  TextEditingController addressController = TextEditingController();

  Rx<DetailSingleModel> detailsSingle = DetailSingleModel().obs;

  var regID = Get.arguments;

  RxBool isLoad = true.obs;

  @override
  void onInit() async {
    formDetail;
    detailSingle(regID: regID);
    typeOffList();
    super.onInit();
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

  void detailSingle({required int regID}) async {
    isLoad(false);
    update();
    Response response;

    var url = "${AppConstants.urlBase}/day-off-letter?regid=${regID}";
    try {
      response = await dio.get(
        url,
      );
      if (response.statusCode == AppConstants.RESPONSE_CODE_SUCCESS) {
        var data = DetailSingleModel.fromJson(response.data);
        detailsSingle.value = data;
        dayController.text = data.rData!.period.toString();
        reasonController.text = data.rData!.reason!;
        addressController.text = data.rData!.address!;
      }
    } catch (e) {
      rethrow;
    } finally {
      Future.delayed(const Duration(seconds: 1), () {
        isLoad(true);
        update();
      });
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

        return data.map((e) => ListOffTypeModel.fromJson(e)).toList();
      } else {
        return [];
      }
    } catch (e) {
      rethrow;
    }
  }

  void typeOffList() async {
    var tokens = await SharePerApi().getToken();
    Response response;
    Map<String, dynamic> headers = {
      HttpHeaders.authorizationHeader: "Bearer $tokens"
    };
    const url = "${AppConstants.urlBase}/${AppConstants.urlListOffType}";
    try {
      response = await dio.get(
        url,
        options: Options(headers: headers),
      );
      if (response.statusCode == 200) {
        List<dynamic> data = response.data["rData"];

        typeOff.value = data.map((e) => ListOffTypeModel.fromJson(e)).toList();
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<List<DayOffLettersSingleModel>> getDayOffLetterSingler(
      {required int needAppr, required String astatus}) async {
    var tokens = await SharePerApi().getToken();
    Response response;
    Map<String, dynamic> headers = {
      HttpHeaders.authorizationHeader: "Bearer $tokens",
    };

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

  void postDetailRegister(
      {required int type,
      required int regID,
      required String reason,
      required String startdate,
      required int period,
      required String address,
      required int command,
      required BuildContext context}) async {
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
        getDayOffLetterSingler(astatus: "", needAppr: 0);
        if (data["rCode"] == 0) {
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
          Get.back(result: true);
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
        }
      }
      update();
    } catch (e) {
      rethrow;
    }
  }
}
