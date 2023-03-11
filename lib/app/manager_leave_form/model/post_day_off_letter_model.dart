class PostDayOffLettersModel {
  int? needAppr;
  String? astatus;

  PostDayOffLettersModel({this.needAppr, this.astatus});

  PostDayOffLettersModel.fromJson(Map<String, dynamic> json) {
    needAppr = json['needAppr'];
    astatus = json['astatus'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['needAppr'] = needAppr;
    data['astatus'] = astatus;
    return data;
  }
}
