class DayOffLettersSingleModel {
  int? empID;
  int? regID;
  int? period;
  String? startDate;
  String? regDate;
  String? type;
  String? address;
  String? reason;
  String? firstName;
  String? lastName;
  String? comeDate;
  String? deptID;
  int? posID;
  int? jPLevel;
  int? apprOrder;
  int? apprState;
  int? aStatus;

  DayOffLettersSingleModel(
      {this.empID,
      this.regID,
      this.period,
      this.startDate,
      this.regDate,
      this.type,
      this.address,
      this.reason,
      this.firstName,
      this.lastName,
      this.comeDate,
      this.deptID,
      this.posID,
      this.jPLevel,
      this.apprOrder,
      this.apprState,
      this.aStatus});

  DayOffLettersSingleModel.fromJson(Map<String, dynamic> json) {
    empID = json['EmpID'];
    regID = json['regID'];
    period = json['Period'];
    startDate = json['StartDate'];
    regDate = json['RegDate'];
    type = json['Type'];
    address = json['Address'];
    reason = json['Reason'];
    firstName = json['FirstName'];
    lastName = json['LastName'];
    comeDate = json['ComeDate'];
    deptID = json['DeptID'];
    posID = json['PosID'];
    jPLevel = json['JPLevel'];
    apprOrder = json['apprOrder'];
    apprState = json['apprState'];
    aStatus = json['aStatus'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['EmpID'] = empID;
    data['regID'] = regID;
    data['Period'] = period;
    data['StartDate'] = startDate;
    data['RegDate'] = regDate;
    data['Type'] = type;
    data['Address'] = address;
    data['Reason'] = reason;
    data['FirstName'] = firstName;
    data['LastName'] = lastName;
    data['ComeDate'] = comeDate;
    data['DeptID'] = deptID;
    data['PosID'] = posID;
    data['JPLevel'] = jPLevel;
    data['apprOrder'] = apprOrder;
    data['apprState'] = apprState;
    data['aStatus'] = aStatus;
    return data;
  }
}
