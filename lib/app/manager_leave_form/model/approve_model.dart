class ApproveModel {
  int? regid;
  String? comment;
  int? state;

  ApproveModel({this.regid, this.comment, this.state});

  ApproveModel.fromJson(Map<String, dynamic> json) {
    regid = json['regid'];
    comment = json['comment'];
    state = json['state'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['regid'] = regid;
    data['comment'] = comment;
    data['state'] = state;
    return data;
  }
}
