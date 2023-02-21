// ignore_for_file: unnecessary_this, unnecessary_brace_in_string_interps

class ListOffTypeModel {
  String? offTypeID;
  String? name;
  String? note;
  int? deletedFlag;

  ListOffTypeModel({this.offTypeID, this.name, this.note, this.deletedFlag});

  ListOffTypeModel.fromJson(Map<String, dynamic> json) {
    offTypeID = json['OffTypeID'];
    name = json['Name'];
    note = json['Note'];
    deletedFlag = json['DeletedFlag'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['OffTypeID'] = offTypeID;
    data['Name'] = name;
    data['Note'] = note;
    data['DeletedFlag'] = deletedFlag;
    return data;
  }

  static List<ListOffTypeModel> fromJsonList(List list) {
    return list.map((item) => ListOffTypeModel.fromJson(item)).toList();
  }

  String offtypeString() {
    return "#${this.name} ${this.note}";
  }

  bool isEqual(ListOffTypeModel model) {
    return this.note == this.note && this.offTypeID == this.offTypeID;
  }

  @override
  String toString() {
    return "${note} (${name})";
  }
}
