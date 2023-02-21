class RegisterDetailModel {
  int? regid;
  int? offtype;
  String? reason;
  String? startdate;
  int? period;
  String? address;
  int? command;

  RegisterDetailModel(
      {this.regid,
      this.offtype,
      this.reason,
      this.startdate,
      this.period,
      this.address,
      this.command});

  RegisterDetailModel.fromJson(Map<String, dynamic> json) {
    regid = json['regid'];
    offtype = json['offtype'];
    reason = json['reason'];
    startdate = json['startdate'];
    period = json['period'];
    address = json['address'];
    command = json['command'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['regid'] = regid;
    data['offtype'] = offtype;
    data['reason'] = reason;
    data['startdate'] = startdate;
    data['period'] = period;
    data['address'] = address;
    data['command'] = command;
    return data;
  }
}
