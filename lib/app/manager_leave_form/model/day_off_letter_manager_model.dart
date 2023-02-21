class DayOffLettersManagerModel {
  int? regID;
  int? empID;
  String? type;
  String? reason;
  String? startDate;
  int? period;
  String? regDate;
  int? annualLeave;
  String? address;
  String? lastName;
  String? firstName;
  String? deptID;
  int? posID;
  int? jPLevel;
  int? apprOrder;
  int? apprState;
  int? aStatus;

  DayOffLettersManagerModel(
      {this.regID,
      this.empID,
      this.type,
      this.reason,
      this.startDate,
      this.period,
      this.regDate,
      this.annualLeave,
      this.address,
      this.lastName,
      this.firstName,
      this.deptID,
      this.posID,
      this.jPLevel,
      this.apprOrder,
      this.apprState,
      this.aStatus});

  DayOffLettersManagerModel.fromJson(Map<String, dynamic> json) {
    regID = json['regID'];
    empID = json['EmpID'];
    type = json['Type'];
    reason = json['Reason'];
    startDate = json['StartDate'];
    period = json['Period'];
    regDate = json['RegDate'];
    annualLeave = json['AnnualLeave'];
    address = json['Address'];
    lastName = json['LastName'];
    firstName = json['FirstName'];
    deptID = json['DeptID'];
    posID = json['PosID'];
    jPLevel = json['JPLevel'];
    apprOrder = json['apprOrder'];
    apprState = json['apprState'];
    aStatus = json['aStatus'];
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
    data['LastName'] = lastName;
    data['FirstName'] = firstName;
    data['DeptID'] = deptID;
    data['PosID'] = posID;
    data['JPLevel'] = jPLevel;
    data['apprOrder'] = apprOrder;
    data['apprState'] = apprState;
    data['aStatus'] = aStatus;
    return data;
  }
}
