class DetailSingleModel {
  int? rCode;
  RData? rData;
  String? rMsg;

  DetailSingleModel({this.rCode, this.rData, this.rMsg});

  DetailSingleModel.fromJson(Map<String, dynamic> json) {
    rCode = json['rCode'];
    rData = json['rData'] != null ? RData.fromJson(json['rData']) : null;
    rMsg = json['rMsg'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['rCode'] = rCode;
    if (rData != null) {
      data['rData'] = rData!.toJson();
    }
    data['rMsg'] = rMsg;
    return data;
  }
}

class RData {
  int? regID;
  int? empID;
  String? type;
  String? reason;
  String? startDate;
  int? period;
  String? regDate;
  int? annualLeave;
  String? address;
  int? aStatus;
  List<ApprInf>? apprInf;

  RData(
      {this.regID,
      this.empID,
      this.type,
      this.reason,
      this.startDate,
      this.period,
      this.regDate,
      this.annualLeave,
      this.address,
      this.aStatus,
      this.apprInf});

  RData.fromJson(Map<String, dynamic> json) {
    regID = json['regID'];
    empID = json['EmpID'];
    type = json['Type'];
    reason = json['Reason'];
    startDate = json['StartDate'];
    period = json['Period'];
    regDate = json['RegDate'];
    annualLeave = json['AnnualLeave'];
    address = json['Address'];
    aStatus = json['aStatus'];
    if (json['apprInf'] != null) {
      apprInf = <ApprInf>[];
      json['apprInf'].forEach((v) {
        apprInf!.add(ApprInf.fromJson(v));
      });
    }
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['regID'] = regID;
    data['EmpID'] = empID;
    data['Type'] = type;
    data['Reason'] = reason;
    data['StartDate'] = startDate;
    data['Period'] = period;
    data['RegDate'] = regDate;
    data['AnnualLeave'] = annualLeave;
    data['Address'] = address;
    data['aStatus'] = aStatus;
    if (apprInf != null) {
      data['apprInf'] = apprInf!.map((v) => v.toJson()).toList();
    }
    return data;
  }
}

class ApprInf {
  int? approvalID;
  int? regID;
  int? apprOrder;
  int? approver;
  int? approJobposID;
  String? comment;
  int? approvalState;
  String? approvalDate;
  String? approDeptID;
  String? approLastName;
  String? approFirstName;
  String? approJobName;
  String? stateName;

  ApprInf(
      {this.approvalID,
      this.regID,
      this.apprOrder,
      this.approver,
      this.approJobposID,
      this.comment,
      this.approvalState,
      this.approvalDate,
      this.approDeptID,
      this.approLastName,
      this.approFirstName,
      this.approJobName,
      this.stateName});

  ApprInf.fromJson(Map<String, dynamic> json) {
    approvalID = json['ApprovalID'];
    regID = json['regID'];
    apprOrder = json['ApprOrder'];
    approver = json['Approver'];
    approJobposID = json['ApproJobposID'];
    comment = json['Comment'];
    approvalState = json['ApprovalState'];
    approvalDate = json['ApprovalDate'];
    approDeptID = json['ApproDeptID'];
    approLastName = json['ApproLastName'];
    approFirstName = json['ApproFirstName'];
    approJobName = json['ApproJobName'];
    stateName = json['StateName'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['ApprovalID'] = approvalID;
    data['regID'] = regID;
    data['ApprOrder'] = apprOrder;
    data['Approver'] = approver;
    data['ApproJobposID'] = approJobposID;
    data['Comment'] = comment;
    data['ApprovalState'] = approvalState;
    data['ApprovalDate'] = approvalDate;
    data['ApproDeptID'] = approDeptID;
    data['ApproLastName'] = approLastName;
    data['ApproFirstName'] = approFirstName;
    data['ApproJobName'] = approJobName;
    data['StateName'] = stateName;
    return data;
  }
}
