class UserModel {
  String? userName;
  String? email;
  int? empID;
  int? status;
  String? lastModify;
  String? firstName;
  String? lastName;
  String? comeDate;
  String? zoneID;
  String? zoneName;
  int? jobPosID;
  int? jPLevelID;
  String? deptID;
  int? annualLeave;
  String? jobpositionName;
  String? jPName;
  String? jPLevelName;
  String? departmentName;

  UserModel({
    this.userName,
    this.email,
    this.empID,
    this.status,
    this.lastModify,
    this.firstName,
    this.lastName,
    this.comeDate,
    this.zoneID,
    this.zoneName,
    this.jobPosID,
    this.jPLevelID,
    this.deptID,
    this.annualLeave,
    this.jobpositionName,
    this.jPName,
    this.jPLevelName,
    this.departmentName,
  });

  UserModel.fromJson(Map<String, dynamic> json) {
    userName = json['UserName'];
    email = json['Email'];
    empID = json['EmpID'];
    status = json['Status'];
    lastModify = json['LastModify'];
    firstName = json['FirstName'];
    lastName = json['LastName'];
    comeDate = json['ComeDate'];
    zoneID = json['ZoneID'];
    zoneName = json['ZoneName'];
    jobPosID = json['JobPosID'];
    jPLevelID = json['JPLevelID'];
    deptID = json['DeptID'];
    annualLeave = json['AnnualLeave'];
    jobpositionName = json['JobpositionName'];
    jPName = json['JPName'];
    jPLevelName = json['JPLevelName'];
    departmentName = json['DepartmentName'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['UserName'] = userName;
    data['Email'] = email;
    data['EmpID'] = empID;
    data['Status'] = status;
    data['LastModify'] = lastModify;
    data['FirstName'] = firstName;
    data['LastName'] = lastName;
    data['ComeDate'] = comeDate;
    data['ZoneID'] = zoneID;
    data['ZoneName'] = zoneName;
    data['JobPosID'] = jobPosID;
    data['JPLevelID'] = jPLevelID;
    data['DeptID'] = deptID;
    data['AnnualLeave'] = annualLeave;
    data['JobpositionName'] = jobpositionName;
    data['JPName'] = jPName;
    data['JPLevelName'] = jPLevelName;
    data['DepartmentName'] = departmentName;
    return data;
  }
}
