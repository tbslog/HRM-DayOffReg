class DayOffLettersSingleModel {
  int? regID;
  int? empID;
  String? type;
  String? reason;
  String? startDate;
  double? period;
  String? regDate;
  String? address;
  String? endDate;
  String? lastName;
  String? firstName;
  String? deptID;
  int? posID;
  String? comeDate;
  int? jPLevel;
  String? jobPositionName;
  String? departmentName;
  String? position;
  int? annualLeave;
  int? apprOrder;
  int? apprState;
  int? aStatus;

  DayOffLettersSingleModel(
      {this.regID,
      this.empID,
      this.type,
      this.reason,
      this.startDate,
      this.period,
      this.regDate,
      this.address,
      this.endDate,
      this.lastName,
      this.firstName,
      this.deptID,
      this.posID,
      this.comeDate,
      this.jPLevel,
      this.jobPositionName,
      this.departmentName,
      this.position,
      this.annualLeave,
      this.apprOrder,
      this.apprState,
      this.aStatus});

  DayOffLettersSingleModel.fromJson(Map<String, dynamic> json) {
    regID = json['regID'];
    empID = json['EmpID'];
    type = json['Type'];
    reason = json['Reason'];
    startDate = json['StartDate'];
    period = json['Period'];
    regDate = json['RegDate'];
    address = json['Address'];
    endDate = json['EndDate'];
    lastName = json['LastName'];
    firstName = json['FirstName'];
    deptID = json['DeptID'];
    posID = json['PosID'];
    comeDate = json['ComeDate'];
    jPLevel = json['JPLevel'];
    jobPositionName = json['JobPositionName'];
    departmentName = json['departmentName'];
    position = json['Position'];
    annualLeave = json['AnnualLeave'];
    apprOrder = json['apprOrder'];
    apprState = json['apprState'];
    aStatus = json['aStatus'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['regID'] = this.regID;
    data['EmpID'] = this.empID;
    data['Type'] = this.type;
    data['Reason'] = this.reason;
    data['StartDate'] = this.startDate;
    data['Period'] = this.period;
    data['RegDate'] = this.regDate;
    data['Address'] = this.address;
    data['EndDate'] = this.endDate;
    data['LastName'] = this.lastName;
    data['FirstName'] = this.firstName;
    data['DeptID'] = this.deptID;
    data['PosID'] = this.posID;
    data['ComeDate'] = this.comeDate;
    data['JPLevel'] = this.jPLevel;
    data['JobPositionName'] = this.jobPositionName;
    data['departmentName'] = this.departmentName;
    data['Position'] = this.position;
    data['AnnualLeave'] = this.annualLeave;
    data['apprOrder'] = this.apprOrder;
    data['apprState'] = this.apprState;
    data['aStatus'] = this.aStatus;
    return data;
  }
}
