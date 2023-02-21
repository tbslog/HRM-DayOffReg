class RegisterModel {
  int? type;
  String? reason;
  String? startdate;
  int? period;
  String? address;
  int? command;

  RegisterModel(
      {this.type,
      this.reason,
      this.startdate,
      this.period,
      this.address,
      this.command});

  RegisterModel.fromJson(Map<String, dynamic> json) {
    type = json['type'];
    reason = json['reason'];
    startdate = json['startdate'];
    period = json['period'];
    address = json['address'];
    command = json['command'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['type'] = type;
    data['reason'] = reason;
    data['startdate'] = startdate;
    data['period'] = period;
    data['address'] = address;
    data['command'] = command;
    return data;
  }
}
