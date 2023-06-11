class OfSubordinatesModel {
  int? empID;
  String? firstName;
  String? lastName;
  String? comeDate;
  String? zoneID;
  String? deptID;
  int? posID;
  int? sex;
  String? tel;
  int? status;
  String? directlyMng;
  String? iDWorkingTime;
  String? name;
  int? jPLevel;

  OfSubordinatesModel(
      {this.empID,
      this.firstName,
      this.lastName,
      this.comeDate,
      this.zoneID,
      this.deptID,
      this.posID,
      this.sex,
      this.tel,
      this.status,
      this.directlyMng,
      this.iDWorkingTime,
      this.name,
      this.jPLevel});

  OfSubordinatesModel.fromJson(Map<String, dynamic> json) {
    empID = json['EmpID'];
    firstName = json['FirstName'];
    lastName = json['LastName'];
    comeDate = json['ComeDate'];
    zoneID = json['ZoneID'];
    deptID = json['DeptID'];
    posID = json['PosID'];
    sex = json['Sex'];
    tel = json['Tel'];
    status = json['Status'];
    directlyMng = json['DirectlyMng'];
    iDWorkingTime = json['IDWorkingTime'];
    name = json['Name'];
    jPLevel = json['JPLevel'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['EmpID'] = empID;
    data['FirstName'] = firstName;
    data['LastName'] = lastName;
    data['ComeDate'] = comeDate;
    data['ZoneID'] = zoneID;
    data['DeptID'] = deptID;
    data['PosID'] = posID;
    data['Sex'] = sex;
    data['Tel'] = tel;
    data['Status'] = status;
    data['DirectlyMng'] = directlyMng;
    data['IDWorkingTime'] = iDWorkingTime;
    data['Name'] = name;
    data['JPLevel'] = jPLevel;
    return data;
  }
}
